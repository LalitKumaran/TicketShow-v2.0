from flask import Blueprint,redirect,request,url_for,jsonify,send_from_directory
from flask_restful import Resource,Api
from flask_jwt_extended import create_access_token, jwt_required
from . import app,db,api,redis_client,cel_app
from .models import User,Venue,Slot,Show,Booking
from sqlalchemy import or_,and_
from datetime import datetime,timedelta
import uuid,json,re,base64,os,csv
from functools import wraps
from celery.result import AsyncResult
from . import tasks

views = Blueprint('views',__name__)


@views.route("/images/<folder>/<filename>")
def get_images(folder,filename):
    image_path = f"static/uploads/{folder}"
    return send_from_directory(image_path,filename)

class LoginAPI(Resource):
    def post(self):
        try:
            client = request.get_json()
            user = User.query.filter_by(user_id=client['email']).first()
            if user:
                if user.check_password(client['password']):
                    access_token = create_access_token(identity=str(user.user_id),expires_delta=timedelta(minutes=30))
                    return {
                        "user":json.dumps({"username": user.username, "email":user.email, "role": user.role, "token": access_token}),
                        "success":True,
                        "msg":"Logged in Successfully"
                        },200
                else:
                    return {
                        "success":"false",
                        "msg":"Wrong Password"
                        },401
            else:
                return {
                    "success":"false",
                    "msg":"User not Found"
                    },404
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
                },500

class RegisterAPI(Resource):
    def post(self):
        try:
            client = request.get_json()
            user = db.session.query(User).filter(or_(User.user_id==client['email'])).first()
            if user:
                return {
                    "success":"false",
                    "msg":"Account exists"
                    },401
            else:
                new_user = User(user_id=client['email'], username=client['username'], email=client['email'], role=client['role'])
                new_user.set_password(client['password'])
                new_user.active = True
                db.session.add(new_user)
                db.session.commit()
                return {
                    "success":"true",
                    "msg":"Registered Successfully"
                },200             
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500

class VenueAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            req = request.get_json()
            venue = db.session.query(Venue).filter(and_(Venue.venue_name==req['theatreName'], Venue.location==req['location'])).first()
            if(venue):
                return {
                        "success":"false",
                        "msg":"Theatre exists"
                },401
            else:
                vid = "V"+str(uuid.uuid4())
                image_data = req['image'].split(',')[1]
                image_filename = req['theatreName'].lower().replace(" ","")
                image_path = f'theatres/{image_filename}.png'
                print(os.getcwd())
                with open("flask/web/static/uploads/"+image_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                venue = Venue(venue_id=vid, venue_name = req['theatreName'], capacity = req['capacity'], location = req['location'], price = req['price'], image=image_path)
                db.session.add(venue)
                db.session.commit()  
                venues = Venue.query.all()
                venue_list = [v.__dict__ for v in venues]
                if redis_client.exists('venue'):
                    redis_client.delete('venue')
                for i in venue_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('venue', str(i))
                venue = redis_client.lrange('venue',0,-1)
                venue = [ eval(v) for v in venue]
                return {
                    "success":"true",
                    "msg":"Theatre Added Successfully"
                },200   
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500
        
    @jwt_required()
    def put(self,venue_id):
        try:
            req = request.get_json()
            venue = Venue.query.get(venue_id)
            if venue:
                venue.venue_name = req['theatreName']
                venue.location = req['location']
                venue.capacity = req['capacity']
                venue.price = req['price']
                venue.image = req['image']
                db.session.commit()
                venues = Venue.query.all()
                venue_list = [v.__dict__ for v in venues]
                if redis_client.exists('venue'):
                    redis_client.delete('venue')
                for i in venue_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('venue', str(i))
                venue = redis_client.lrange('venue',0,-1)
                venue = [ eval(v) for v in venue]
                return {
                    "success":"true",
                    "msg":"Theatre Updated Successfully"
                },200
            else:
                return {
                    "success":"false",
                    "msg":"Theatre Doesn't Exist"
                },404
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500
        
    @jwt_required()
    def delete(self,theatreId):
        try:
            venue = Venue.query.get(theatreId)
            if venue:
                slots = Slot.query.filter_by(venue_id = theatreId)
                bookings = Booking.query.filter_by(venue_id = theatreId)
                for b in bookings:
                    b.status = "Cancelled"
                    b.slot_id = None
                    b.venue_id = None
                    db.session.commit()
                for s in slots:
                    db.session.delete(s)
                db.session.delete(venue)
                db.session.commit()
                venues = Venue.query.all()
                venue_list = [v.__dict__ for v in venues]
                if redis_client.exists('venue'):
                    redis_client.delete('venue')
                for i in venue_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('venue', str(i))
                venue = redis_client.lrange('venue',0,-1)
                venue = [ eval(v) for v in venue]
                return {
                    "success":"true",
                    "msg":"Theatre Deleted Successfully"
                },200
            else:
                return {
                    "success":"false",
                    "msg":"Theatre Doesn't Exist"
                },404
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500

class ShowAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            req = request.get_json()
            if(req['show_id']):
                sid = req['show_id']
            else:
                sid = "S"+str(uuid.uuid4())
                poster_data = req['poster'].split(',')[1]
                poster_filename = req['show_name'].lower().replace(" ","")
                poster_path = f"shows/{poster_filename}.png"
                with open("flask/web/static/uploads/"+poster_path, 'wb') as f:
                    f.write(base64.b64decode(poster_data))
                new_show = Show(show_id=sid,show_name=req['show_name'], rating=req['rating'], lang=req['lang'], tag=req['tag'], duration = req['duration'], cast=req['cast'], poster=poster_path)
                db.session.add(new_show)
            slid = "SL"+str(uuid.uuid4())
            slot = Slot(slot_id=slid, show_id=sid, venue_id=req['venue'], date=datetime.strptime(req['date'], "%Y-%m-%d").date(), time=datetime.strptime(req['time'], "%H:%M").time(), seats_available=req['seats_available'], duration=re.search(r'\d+', req['duration']).group())
            db.session.add(slot)
            db.session.commit()
            shows = Show.query.all()
            show_list = [s.__dict__ for s in shows]
            if redis_client.exists('show'):
                redis_client.delete('show')
            for i in show_list:
                i.pop('_sa_instance_state')
                redis_client.rpush('show', str(i))
            show = redis_client.lrange('show',0,-1)
            show = [ eval(s) for s in show]
            slots = Slot.query.all()
            slot_list = [s.__dict__ for s in slots]
            if redis_client.exists('slot'):
                redis_client.delete('slot')
            for i in slot_list:
                i.pop('_sa_instance_state')
                i['time'] = i['time'].strftime("%H:%M")
                i['date'] = i['date'].strftime("%Y-%m-%d")
                redis_client.rpush('slot', str(i))
            slot = redis_client.lrange('slot',0,-1)
            slot = [ eval(sl) for sl in slot ]
            return {
                "success":"true",
                "msg":"Show Added Successfully"
            },200
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500
        
    @jwt_required()
    def put(self,show_id):
        try:
            req = request.get_json()
            show = Show.query.get(show_id)
            if show:
                show.show_name = req['show_name']
                show.tag = req['tag']
                show.rating = req['rating']
                show.lang = req['lang']
                show.cast = req['cast']
                show.duration = req['duration']
                show.poster = req['poster']
                db.session.commit()
                shows = Show.query.all()
                show_list = [s.__dict__ for s in shows]
                if redis_client.exists('show'):
                    redis_client.delete('show')
                for i in show_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('show', str(i))
                show = redis_client.lrange('show',0,-1)
                show = [ eval(s) for s in show]
                return {
                    "success":"true",
                    "msg":"Show Updated Successfully"
                },200
            else:
                return {
                    "success":"false",
                    "msg":"Show Doesn't Exist"
                },404
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500

    @jwt_required()
    def delete(self,show_id):
        try:
            show = Show.query.get(show_id)
            if show:
                slots = Slot.query.filter_by(show_id = show_id)
                bookings = Booking.query.filter_by(show_id = show_id)
                for b in bookings:
                    b.status = "Cancelled"
                    b.slot_id = None
                    b.show_id = None
                for s in slots:
                    db.session.delete(s)
                db.session.delete(show)
                db.session.commit()
                slots = Slot.query.all()
                slot_list = [s.__dict__ for s in slots]
                if redis_client.exists('slot'):
                    redis_client.delete('slot')
                for i in slot_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    redis_client.rpush('slot', str(i))
                redis_client.expire('slot',1800)
                slot = redis_client.lrange('slot',0,-1)
                slot = [ eval(sl) for sl in slot ]
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                if redis_client.exists('booking'):
                    redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    i['booking_time'] = i['booking_time'].strftime("%H:%M")
                    i['booking_date'] = i['booking_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                redis_client.expire('booking',1800)
                booking = redis_client.lrange('booking',0,-1)
                booking = [ eval(b) for b in booking]
                return {
                    "success":"true",
                    "msg":"Show Deleted Successfully"
                },200
            else:
                return {
                    "success":"false",
                    "msg":"Show Doesn't Exist"
                },404

        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500


class FetchAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            if redis_client.exists('venue'):
                venue = redis_client.lrange('venue',0,-1)
            else:
                venues = Venue.query.all()
                venue_list = [v.__dict__ for v in venues]
                redis_client.delete('venue')
                for i in venue_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('venue', str(i))
                venue = redis_client.lrange('venue',0,-1)
                redis_client.expire('venue',1800)
            venue = [ eval(v) for v in venue]

            if redis_client.exists('show'):
                show = redis_client.lrange('show',0,-1)
            else:
                shows = Show.query.all()
                show_list = [s.__dict__ for s in shows]
                redis_client.delete('show')
                for i in show_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('show', str(i))
                show = redis_client.lrange('show',0,-1)
                redis_client.expire('show',1800)
            show = [ eval(s) for s in show]

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
            slot = [ eval(sl) for sl in slot ]

            if redis_client.exists('booking'):
                booking = redis_client.lrange('booking',0,-1)
            else:
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    i['booking_time'] = i['booking_time'].strftime("%H:%M")
                    i['booking_date'] = i['booking_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                booking = redis_client.lrange('booking',0,-1)
                redis_client.expire('booking',1800)
            booking = [ eval(b) for b in booking]

            response_data = {
                "venues": venue,
                "shows": show,
                "slots": slot,
                "bookings": booking,
                "success": "true",
                "msg": "Data fetch successful"
            }

            return response_data, 200
        
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500


class BookingAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            req = request.get_json()
            user = User.query.filter_by(user_id=req['user_id']).first()
            if(user):
                slot = Slot.query.filter_by(slot_id=req['slot_id']).first()
                bid = 'B'+ str(uuid.uuid4())
                booking = Booking(booking_id = bid, user_id = req['user_id'],status="Confirmed", booking_date=datetime.now().date(), booking_time=datetime.now().time(),date=datetime.strptime(req['date'], "%Y-%m-%d").date(), time=datetime.strptime(req['time'], "%H:%M").time(), msg="", slot_id=req['slot_id'],seat_count=req['seat_count'], amount = req['amount'], show_id = slot.show_id, venue_id = slot.venue_id)
                slot.seats_available -= int(req['seat_count'])
                db.session.add(booking)
                db.session.commit()
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                if redis_client.exists('booking'):
                    redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    i['booking_time'] = i['booking_time'].strftime("%H:%M")
                    i['booking_date'] = i['booking_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                booking = redis_client.lrange('booking',0,-1)
                booking = [ eval(b) for b in booking]
                return {
                    "success":"true",
                    "msg":"Booking Successful",
                },200
            else:
                return {
                    "success":"flase",
                    "msg":"User Not Found",
                },404
        except Exception as e:
            print(e)
            return {
                "success":"flase",
                "msg":"Invalid Server Error",
            },500
        
    @jwt_required()
    def put(self):
        try:
            req = request.get_json()
            booking = Booking.query.filter_by(booking_id = req['booking_id']).first()
            if booking:
                booking.user_rating = req['user_rating']
                db.session.commit()
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                if redis_client.exists('booking'):
                    redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    i['booking_time'] = i['booking_time'].strftime("%H:%M")
                    i['booking_date'] = i['booking_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                booking = redis_client.lrange('booking',0,-1)
                booking = [ eval(b) for b in booking]
            else:
                return {
                    "success":"true",
                    "msg":"Booking Doesn't Exist"
                },404
            show = Show.query.filter_by(show_id=req['show_id']).first()
            if show:
                show.rating = (show.rating + req['user_rating'])/2
                db.session.commit()
                shows = Show.query.all()
                show_list = [s.__dict__ for s in shows]
                if redis_client.exists('show'):
                    redis_client.delete('show')
                for i in show_list:
                    i.pop('_sa_instance_state')
                    redis_client.rpush('show', str(i))
                show = redis_client.lrange('show',0,-1)
                show = [ eval(s) for s in show]
            return {
                    "success":"true",
                    "msg":"Thanks for rating"
                },200
        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500
        
    @jwt_required()
    def delete(self):
        try:
            req = request.get_json()
            booking_id = req['booking_id']
            booking = Booking.query.get(booking_id)
            if booking:
                slot = Slot.query.get(req['slot_id'])
                slot.seats_available += req['seat_count']
                booking.status = "Cancelled"
                db.session.commit()
                slots = Slot.query.all()
                slot_list = [s.__dict__ for s in slots]
                if redis_client.exists('slot'):
                    redis_client.delete('slot')
                for i in slot_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    redis_client.rpush('slot', str(i))
                slot = redis_client.lrange('slot',0,-1)
                slot = [ eval(sl) for sl in slot ]
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                if redis_client.exists('booking'):
                    redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    i['booking_time'] = i['booking_time'].strftime("%H:%M")
                    i['booking_date'] = i['booking_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                booking = redis_client.lrange('booking',0,-1)
                booking = [ eval(b) for b in booking]
                return {
                    "success":"true",
                    "msg":"Booking cancelled Successfully"
                },200
            else:
                return {
                    "success":"true",
                    "msg":"Booking Doesn't Exist"
                },404

        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500

class SlotAPI(Resource):
    @jwt_required()
    def delete(self,slot_id):
        try:
            slot = Slot.query.get(slot_id)
            booking = Booking.query.all()
            if slot:
                for b in booking:
                    if b.slot_id == slot_id:
                        b.status = "Cancelled"
                        b.slot_id = None
                db.session.delete(slot)
                db.session.commit()
                slots = Slot.query.all()
                slot_list = [s.__dict__ for s in slots]
                if redis_client.exists('slot'):
                    redis_client.delete('slot')
                for i in slot_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    redis_client.rpush('slot', str(i))
                slot = redis_client.lrange('slot',0,-1)
                slot = [ eval(sl) for sl in slot ]
                bookings = Booking.query.all()
                booking_list = [b.__dict__ for b in bookings]
                if redis_client.exists('booking'):
                    redis_client.delete('booking')
                for i in booking_list:
                    i.pop('_sa_instance_state')
                    i['time'] = i['time'].strftime("%H:%M")
                    i['date'] = i['date'].strftime("%Y-%m-%d")
                    i['booking_time'] = i['booking_time'].strftime("%H:%M")
                    i['booking_date'] = i['booking_date'].strftime("%Y-%m-%d")
                    redis_client.rpush('booking', str(i))
                booking = redis_client.lrange('booking',0,-1)
                booking = [ eval(b) for b in booking]
                return {
                    "success":"true",
                    "msg":"Show Cancelled Successfully"
                },200
            else:
                return {
                    "success":"false",
                    "msg":"Show Doesn't Exist"
                },404

        except Exception as e:
            print(e)
            return {
                "success":"false",
                "msg":"Invalid server Error"
            },500
        
api.add_resource(LoginAPI,"/api/login")
api.add_resource(RegisterAPI,"/api/register")
api.add_resource(VenueAPI,"/api/venue","/api/venue/<theatreId>")
api.add_resource(ShowAPI,"/api/show","/api/show/<show_id>")
api.add_resource(SlotAPI,"/api/cancel/show/<slot_id>")
api.add_resource(FetchAPI,"/api/fetch")
api.add_resource(BookingAPI,"/api/bookshow","/api/ratebooking")


from flask_mail import Message
from . import mail,app
@views.post('/exportvenue')
@jwt_required()
def exportCSV():
    try:
        req = request.get_json()
        user = req['user']
        venue = req['venue']
        field_names = ['Show Name', 'Date', 'Time', 'Bookings', 'Rating', 'Total Revenue']
        slots = Slot.query.filter_by(venue_id = venue['venue_id']).order_by(Slot.date,Slot.time).all()
        csv_name = venue['venue_name'].lower().replace(" ","")
        csv_filename = os.path.join('flask/web/static/exports/', f"{csv_name}.csv")
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for slot in slots:
                show = Show.query.filter_by(show_id = slot.show_id).first()
                bookings = Booking.query.filter_by(slot_id = slot.slot_id).all()
                revenue = 0
                for b in bookings:
                    revenue += b.amount
                writer.writerow({
                    'Show Name': show.show_name,
                    'Date': slot.date,
                    'Time': slot.time,
                    'Bookings': venue['capacity']-slot.seats_available,
                    'Rating': show.rating,
                    'Total Revenue': revenue,
                })
        s = tasks.export_csv_to_user.apply_async((csv_filename,user,venue))
        # s = tasks.alert_user.apply_async(())
        return {
                "success":"true",
                "msg":"File generated",
                "task_id": str(s),
            },200
    except Exception as e:
        print(e)
        return {
                "success":"false",
                "msg":"Invalid server Error",
            },500
    
@views.get("/exportvenue/checkstatus/<task_id>")
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

