import os
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import crontab
from .worker import create_celery_app
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
import redis
from .config import LocalDevelopmentConfig
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
db = SQLAlchemy()
api = Api(app)
mail = Mail(app)
cache = Cache(app)
mailid = "22f2001140@ds.study.iitm.ac.in"   
cel_app = create_celery_app(app)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
redis_client.flushdb()

def create_app():
    app.config['DEBUG'] = True
    app.config['SQLITE_DB_DIR'] = os.path.join(basedir, "../db_directory")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = "ticketshow"
    app.config['JWT_SECRET_KEY'] = "ticketshow"
    # app.config['SECRET_KEY'] = "idfqoiehjasDBt?9D8~J7!3AJOSIDFJM,ENfchuO[yKW8XU|{dlZ:k|ZTZI,BCg"
    # app.config['JWT_SECRET_KEY'] = "awuefiibiawlueu923afwmk"
    app.config['ADMIN_PASSWORD'] = "12345678"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "22f2001140@ds.study.iitm.ac.in"
    app.config['MAIL_PASSWORD'] = "sjwsandapiszibqp"
    # app.app_context().push()
    if os.getenv('ENV','development') == 'production':
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting local development environment")
        app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()
    
    db.init_app(app)
    api.init_app(app)
    JWTManager(app)
    mail = Mail(app)

    
    from .tasks import alert_user,monthly_report
    @cel_app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        # Executes every day at 6:30 p.m.
        sender.add_periodic_task(
            crontab(hour=18, minute=28),
            alert_user.s(),
        )
        sender.add_periodic_task(
            # First day of every month at 7:00 am
            crontab(day_of_month=1, hour=7, minute=00),  
            monthly_report.s(),
        )


    from .api import views
    app.register_blueprint(views, url_prefix='/')

    # CORS(app, resources={r'/*':{'origins':'*'}})
    # app.config['CORS_HEADERS'] = 'Content-Type'
    # app.app_context().push()
    CORS(app, support_credentials=True)

    
    with app.app_context():
        db.create_all()
        from .models import User
        admin = User.query.filter_by(email=mailid).first()
        if admin is None:
            admin = User(username="Admin", email=mailid, password=generate_password_hash(app.config['ADMIN_PASSWORD'], method='scrypt'), role="admin")
            db.session.add(admin)
            db.session.commit()

    return app