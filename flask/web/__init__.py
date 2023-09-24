from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from .worker import create_celery_app
import redis,os
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "database.db"

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
mail = Mail(app)
cel_app = create_celery_app(app)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
redis_client.flushdb()

def createapp():  
  
    #config for mail
    app.config['DEBUG'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    mail = Mail(app)

    #celery scheduled jobs
    from .tasks import alert_user,monthly_report
    @cel_app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        # Executes every day at 6:30 p.m.
        sender.add_periodic_task(
            crontab(hour=5, minute=9),
            alert_user.s(),
        )
        sender.add_periodic_task(
            # First day of every month at 7:00 am
            crontab(hour=5, minute=10),  
            monthly_report.s(),
        )
    
    #config for DB
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 

    #config for JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    #config for admin
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD')

    #cors enabling
    CORS(app, resources={r'/*':{'origins':'*'}})
    
    #Initializing db
    db.init_app(app)
    api.init_app(app)
    
    #JWTsetup
    JWTManager(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        db.create_all()
        from .models import User
        admin = User.query.filter_by(email="22f2001140@ds.study.iitm.ac.in").first()
        if admin is None:
            admin = User(user_id="22f2001140@ds.study.iitm.ac.in", username="lalit", email="22f2001140@ds.study.iitm.ac.in", role="admin")
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
    return app

