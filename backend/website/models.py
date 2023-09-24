from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    role = db.Column(db.String, nullable=False)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text)
    slots = db.relationship("Slot", backref="slot", lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(150), nullable=False)
    stars = db.Column(db.String(150), nullable=False)
    language = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text)
    rating = db.Column(db.String(150))
    no_of_users_rated = db.Column(db.Integer,default=0)
    showing = db.Column(db.Boolean, default=True)

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    remaining_seats = db.Column(db.Integer, nullable=False)
    bookings = db.relationship("Booking", backref="booking", lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    no_of_tickets = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    booked_date = db.Column(db.Date, default=datetime.date.today)
    user_rating = db.Column(db.Integer, default=0)
    status = db.Column(db.String(150), nullable=False)


