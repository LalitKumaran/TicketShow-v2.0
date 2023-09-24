from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    user_id = db.Column(db.String(150), primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable=False,unique=True)
    password = db.Column(db.String(150), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    role = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Venue(db.Model):
    venue_id = db.Column(db.String(150), primary_key=True)
    venue_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text)
    price = db.Column(db.Integer)
    shows = db.relationship("Slot", backref="slot", lazy=True)

class Show(db.Model):
    show_id = db.Column(db.String(150), primary_key=True)
    show_name = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Numeric(precision=8, scale=2, asdecimal=False))
    tag = db.Column(db.String(150))
    cast = db.Column(db.String(200))
    lang = db.Column(db.String(150),nullable=False)
    duration = db.Column(db.String(150), nullable=False)
    poster = db.Column(db.Text)
    slots = db.relationship('Slot', backref="show", lazy=True)

class Slot(db.Model):
    slot_id = db.Column(db.String(150), primary_key=True)
    show_id = db.Column(db.String(150), db.ForeignKey('show.show_id'), nullable=False)
    venue_id = db.Column(db.String(150),db.ForeignKey('venue.venue_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.String(150),nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    booking_id = booking_id = db.Column(db.String(150), primary_key=True)
    seat_count = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_rating = db.Column(db.Integer,default=0)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    msg = db.Column(db.String(500))
    status = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.String(150), db.ForeignKey('user.user_id'), nullable=False)
    slot_id = db.Column(db.String(150), db.ForeignKey('slot.slot_id'))
    show_id = db.Column(db.String(150), db.ForeignKey('show.show_id'))
    venue_id = db.Column(db.String(150),db.ForeignKey('venue.venue_id'))
    
    

