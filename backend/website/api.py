from flask_restful import Resource, fields, reqparse
from flask import Blueprint,redirect,request,url_for,jsonify,send_from_directory
from . import app, api, mail, db, cache, redis_client
from flask_jwt_extended import create_access_token, jwt_required
from flask import redirect,request,url_for,jsonify,send_from_directory,make_response
from .models import *
from sqlalchemy import and_
import base64
from  werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from celery.result import AsyncResult
from datetime import datetime,timedelta
import json
import pathlib
from pathlib import Path
from datetime import timedelta
from .tasks import export_csv_to_user,alert_user,monthly_report
import os
import csv

views = Blueprint('views',__name__)


@views.route("/images/<folder>/<filename>")
def get_images(folder,filename):
    image_path = f"static/{folder}"
    return send_from_directory(image_path,filename)



class Error(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":error_code, "error_message":error_message, "status":status_code, "success":"false"}
        self.response = make_response(json.dumps(message), status_code)


class UserAPI(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {
                    "user":json.dumps({"username": user.username, "email":user.email, "active": user.active, "role": user.role}),
                    "success":True,
                    "msg":"Fetched User"
                },200
        else:
            raise Error(400,"USER_DOES_NOT_EXIST","User not found")

    def post(self):
        data = request.get_json()
        exist = User.query.filter(User.email == data['email']).first()
        if exist:
            raise Error(400,"EMAIL_ALREADY_EXISTS","Email Already Exists")
        else:
            new_user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password'],method='scrypt'), role=data['role'])
            new_user.active = True
            db.session.add(new_user)
            db.session.commit()
            return {
                    "success":True,
                    "msg":"Registered"
                },200

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.email == data['email']).first()
        if user:
            if check_password_hash(user.password, data['password']):
                access_token = create_access_token(identity=str(user.id)+str(user.email), expires_delta=timedelta(minutes=30))
                return {
                        "user":json.dumps({"user_id":user.id,"username": user.username, "email":user.email, "role": user.role, "token": access_token}),
                        "success":True,
                        "msg":"Logged In"
                    },200
            else:
                raise Error(400,"WRONG_PASSWORD","Wrong Password")
            
        else:
            raise Error(400,"USER_DOES_NOT_EXIST","User not found")


class TheatreAPI(Resource):
    @jwt_required()
    def get(self, theatre_id):
        theatre = User.query.filter(User.id == theatre_id).first()
        if theatre:
            return theatre
        else:
            raise Error(400,"THEATRE_DOES_NOT_EXIST","Theatre not found")
        
    @jwt_required()
    def post(self):
        print("hi from post theatre")
        data = request.get_json()
        theatre = Theatre.query.filter(and_(Theatre.name == data['name'], Theatre.city == data['city'] )).first()
        if theatre:
            raise Error(400,"THEATRE_ALREADY_EXISTS","Theatre Already Exists")
        else:
            image_data = data['image'].split(',')[1]
            image_filename = data['name'].lower().replace(" ","")
            image_path = f'{image_filename}.png'
            with open("backend/website/static/theatre/"+image_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
            theatre = Theatre(name = data['name'], city = data['city'], seats = data['seats'], price = data['price'], image=image_path)
            db.session.add(theatre)
            db.session.commit()

            return {
                    "success":True,
                    "msg":"Theatre Added"
                },200
        
    @jwt_required()
    def put(self, theatre_id):
        data = request.get_json()
        theatre = Theatre.query.filter(Theatre.id == theatre_id).first()
        if theatre:
            theatre.name = data['name']
            theatre.city = data['city']
            theatre.seats = data['seats']
            theatre.price = data['price']
            image_data = data['image'].split(',')[1]
            image_filename = data['name'].lower().replace(" ","")
            image_path = f'{image_filename}.png'
            with open("backend/website/static/theatre/"+image_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
            theatre.image = image_path
            db.session.commit()

            return{
                    "success":True,
                    "msg":"Theatre Updated"    
                }
        else:
            raise Error(400,"THEATRE_DOES_NOT_EXIST","Theatre not found")
        
    @jwt_required()
    def delete(self, theatre_id):
        theatre = Theatre.query.filter(Theatre.id == theatre_id).first()
        if theatre:
            slots = Slot.query.filter(Slot.theatre_id == theatre_id)
            bookings = Booking.query.filter(Booking.theatre_id == theatre_id)
            for booking in bookings:
                booking.status = "Cancelled"
                booking.slot_id = None
                booking.theatre_id = None
            for slot in slots:
                db.session.delete(slot)
            db.session.delete(theatre)
            db.session.commit()

            return{
                    "success":True,
                    "msg":"Theatre Deleted"    
                }
        else:
            raise Error(400,"THEATRE_DOES_NOT_EXIST","Theatre not found")
        

class MovieAPI(Resource):
    @jwt_required()
    def get(self, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie:
            return{
                    "movie":json.dumps({"title": movie.title, "genre": movie.genre, "director": movie.director, "stars": movie.stars, "language": movie.language, "rating": movie.rating, "duration": movie.duration, "image": movie.image}),
                    "success":True,
                    "msg":"Fetched Movie"
                },200
        else:
            raise Error(400,"MOVIE_DOES_NOT_EXIST","Movie not found")

    @jwt_required()    
    def post(self):
        data = request.get_json()
        movie = Movie.query.filter(and_(Movie.title == data['title'], Movie.director == data['director'] )).first()
        if movie:
            raise Error(400,"MOVIE_ALREADY_EXISTS","Movie Already Exists")
        else:
            image_data = data['image'].split(',')[1]
            image_filename = data['title'].lower().replace(" ","")
            image_path = f'{image_filename}.png'
            with open("backend/website/static/movie/"+image_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
            movie = Movie(title = data['title'], genre = data['genre'], director = data['director'], stars = data['stars'], language = data['language'], rating = data['rating'], duration = data['duration'], image=image_path)
            db.session.add(movie)
            db.session.commit()
            theatre = Theatre.query.filter(Theatre.id == data['theatre_id'])
            movie = Movie.query.filter(and_(Movie.title == data['title'], Movie.director == data['director'] )).first()
            slot = Slot(theatre_id=data['theatre_id'], movie_id=movie.id, date=data['date'], time=data['time'], remaining_seats=theatre.seats)
            db.session.add(slot)
            db.session.commit()

            return {
                    "success":True,
                    "msg":"Movie Added"
                },200
        
    @jwt_required()
    def put(self, movie_id):
        data = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie:
            movie.title = data['title']
            movie.genre = data['genre']
            movie.director = data['director']
            movie.stars = data['stars']
            movie.language = data['language']
            movie.duration = data['duration']
            movie.rating = data['rating']
            if len(data['image'].split(',')) > 1:
                image_data = data['image'].split(',')[1]
                image_filename = data['title'].lower().replace(" ","")
                image_path = f'{image_filename}.png'
                with open("backend/website/static/movie/"+image_path, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                movie.image = image_path
            else:
                movie.image = data['image']

            db.session.commit()

            return{
                    "success":True,
                    "msg":"Movie Updated"    
                }
        else:
            raise Error(400,"MOVIE_DOES_NOT_EXIST","Movie not found")
        
    @jwt_required()
    def delete(self, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie:
            slots = Slot.query.filter_by(movie_id = movie_id)
            bookings = Booking.query.filter_by(movie_id = movie_id)
            for booking in bookings:
                booking.status = "Cancelled"
                booking.slot_id = None
                booking.movie_id = None
            for s in slots:
                db.session.delete(s)
            db.session.delete(movie)
            db.session.commit()
            return{
                    "success":True,
                    "msg":"Movie Deleted"    
                }
        else:
            raise Error(400,"MOVIE_DOES_NOT_EXIST","Movie not found")
        

class SlotAPI(Resource):
    @jwt_required()
    def get(self, slot_id):
        slot = Slot.query.get(slot_id)
        if slot:
            movie = Movie.query.filter(Movie.id == slot.movie_id)
            theatre = Theatre.query.filter(Theatre.id == slot.theatre_id)
            return{
                "movie":json.dumps({"title": movie.title, "theatre": theatre.name, "date": slot.date, "time": slot.time, "remaining_seats": slot.remaining_seats}),
                "success":True,
                "msg":"Fetched Slot"
            }
        else:
            raise Error(400,"SLOT_DOES_NOT_EXIST","Slot not found")
    
    def post(self):
        data = request.get_json()
        slot = Slot(theatre_id=data['theatre_id'], movie_id=data['movie_id'], date=datetime.datetime.strptime(data['date'], "%Y-%m-%d").date(), time=datetime.datetime.strptime(data['time'], "%H:%M").time(), remaining_seats=data['remaining_seats'])
        db.session.add(slot)
        db.session.commit()

        return{
            "success": True,
            "msg": "Slot Added"
        }
    
    def delete(self, slot_id):
        slot = Slot.query.get(slot_id)
        booking = Booking.query.all()
        if slot:
            for b in booking:
                if b.slot_id == slot_id:
                    b.status = "Cancelled"
                    b.slot_id = None
            db.session.delete(slot)
            db.session.commit()

            return{
                "success":True,
                "msg": "Slot Cancelled"
            }
        
        else:
            raise Error(400,"SLOT_DOES_NOT_EXIST","Slot not found")


class BookingAPI(Resource):
    @jwt_required()
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            movie = Movie.query.filter(Movie.id == booking.movie_id)
            theatre = Theatre.query.filter(Theatre.id == booking.theatre_id)
            slot = Slot.query.filter(Slot.id == booking.slot_id)
            return{
                    "booking":json.dumps({"movie": movie.title, "theatre": theatre.name, "city": theatre.city, "date": slot.date.strftime("%H:%M"), "time": slot.time.strftime("%Y-%m-%d"), "no_of_ticket": booking.ticket, "cost": booking.cost, "status": booking.status, "user_rating": booking.user_rating}),
                    "success":True,
                    "msg":"Fetched Booking"
                },200
        
    @jwt_required()
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.email == data['email']).first()
        slot = Slot.query.filter(Slot.id == data['slot_id']).first()
        if int(data['no_of_tickets']) > slot.remaining_seats:
            return{
                "success":False,
                "msg":"Housefull"
            },200
        else:
            booking = Booking(user_id=user.id, slot_id=slot.id, movie_id=slot.movie_id, theatre_id=slot.theatre_id, no_of_tickets=data['no_of_tickets'], cost=data['cost'], status="Confirmed")
            slot.remaining_seats -= int(data['no_of_tickets'])
            db.session.add(booking)
            db.session.commit()

            return{
                "success":True,
                "msg":"Booking Confirmed"
            }

    @jwt_required()
    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            slot = Slot.query.get(booking.slot_id)
            slot.seats_available += booking.no_of_tickets
            booking.status = "Cancelled"
            db.session.commit()
            return{
                "success": True,
                "msg": "Booking Cancelled"
            }
        else:
            raise Error(400,"BOOKING_DOES_NOT_EXIST","Booking not found")
    
class RatingAPI(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        booking = Booking.query.get(data['booking_id'])
        if booking:
            booking.user_rating = data['user_rating']
            movie = Movie.query.filter(Movie.id == booking.movie_id).first()
            current = movie.rating
            new = (current*(movie.no_of_users_rated) + data['user_rating'])/(movie.no_of_users_rated + 1) 
            movie.no_of_users_rated += 1
            movie.rating = new
            db.session.commit()

            return{
                "success": True,
                "msg": "Rating Added"
            }
        else:
            raise Error(400,"BOOKING_DOES_NOT_EXIST","Booking not found")
        

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FetchAllAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            if redis_client.exists('theatre'):
                theatre = redis_client.lrange('theatre',0,-1)
            else:
                theatres = Theatre.query.all()
                theatre_list = [t.__dict__ for t in theatres]
                redis_client.delete('theatre')
                for i in theatre_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('theatre', str(i))
                theatre = redis_client.lrange('theatre',0,-1)
                redis_client.expire('theatre',1800)
            theatre_list = [ eval(v) for v in theatre]

            if redis_client.exists('movie'):
                movie = redis_client.lrange('movie',0,-1)
            else:
                movies = Movie.query.all()
                movie_list = [m.__dict__ for m in movies]
                redis_client.delete('movie')
                for i in movie_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('movie', str(i))
                movie = redis_client.lrange('movie',0,-1)
                redis_client.expire('movie',1800)
            movie_list = [ eval(m) for m in movie]

            if redis_client.exists('slot'):
                slot = redis_client.lrange('slot',0,-1)
            else:
                slots = Slot.query.all()
                slot_list = [s.__dict__ for s in slots]
                redis_client.delete('slot')
                for i in slot_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    redis_client.rpush('slot', str(i))
                slot = redis_client.lrange('slot',0,-1)
                redis_client.expire('slot',1800)
            slot_list = [ eval(sl) for sl in slot ]

            if redis_client.exists('booking'):
                booking = redis_client.lrange('booking',0,-1)
            else:
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['booked_date'] = i['booked_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                booking = redis_client.lrange('booking',0,-1)
                redis_client.expire('booking',1800)
            booking_list = [ eval(b) for b in booking]

            data = {
                    "theatre": json.dumps(theatre_list),
                    "movie": json.dumps(movie_list),
                    "slots": json.dumps(slot_list),
                    "bookings": json.dumps(booking_list),
                    "success": "true",
                    "msg": "Data Fetched"
            }
            print(data)

            return data, 200
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error",
            },500

            

@views.post('/exportStats')
@jwt_required()
def exportCSV():
    try:
        req = request.get_json()
        user = req['user']
        theatre = req['theatre']
        field_names = ['Movie Name', 'Date', 'Time', 'Bookings', 'Rating']
        slots = Slot.query.filter_by(theatre_id = theatre['id']).order_by(Slot.date,Slot.time).all()
        csv_name = theatre['name'].lower().replace(" ","")
        filename = os.path.join('backend/website/static/exports/', f"{csv_name}.csv")
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for slot in slots:
                movie = Movie.query.filter_by(id = slot.movie_id).first()
                bookings = Booking.query.filter_by(slot_id = slot.id).all()
                writer.writerow({
                    'Movie Name': movie.title,
                    'Date': slot.date,
                    'Time': slot.time,
                    'Bookings': theatre['seats']-slot.remaining_seats,
                    'Rating': movie.rating,
                })
        taskId = export_csv_to_user.apply_async((filename,user,theatre))
        return {
                "success":"true",
                "msg":"File generated",
                "task_id": str(taskId),
            },200
    except Exception as e:
        print(e)
        return {
                "success":"false",
                "msg":"Invalid server Error",
            },500

@views.get("/exportStats/checkStatus/<task_id>")
@jwt_required()
def check_status(task_id):
    try:
        res = AsyncResult(task_id)
        if res.ready():
            return res.result,200
        else:
            return {
                "success":"false",
                "ready": "false",
                "msg":"Export on process"
            },200
        
    except Exception as e:
        print(e)
        return {
                "success":"false",
                "msg":"Invalid server Error",
            },500 

api.add_resource(LoginAPI,"/api/login")
api.add_resource(UserAPI,"/api/register","/api/get/<int:user_id>")
api.add_resource(TheatreAPI,"/api/theatre","/api/theatre/<int:theatre_id>")
api.add_resource(MovieAPI,"/api/movie","/api/movie/<int:movie_id>")
api.add_resource(SlotAPI,"/api/slot/<int:slot_id>","/api/slot")
api.add_resource(FetchAllAPI,"/api/fetch")
api.add_resource(BookingAPI,"/api/booking","/api/cancelbooking/<int:booking_id>")
api.add_resource(RatingAPI,"/api/giveRating")