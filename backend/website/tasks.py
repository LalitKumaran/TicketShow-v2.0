from celery import shared_task
from flask import render_template_string
import csv,os
from flask_mail import Message
from . import db,mail,app,cel_app,create_app
from .models import Booking,User,Movie,Theatre,Slot
import datetime


@shared_task(ignore_result=False)
def export_csv_to_user(filename,user,theatre):
    try:
        subject = f"CSV Report for {theatre['name']}"
        body = f"Export for theatre {theatre['name']}"
        msg = Message(subject=subject,sender="22f2001140@ds.study.iitm.ac.in",recipients=[user['email']])
        msg.body = body
        with app.open_resource('../../'+filename) as file: msg.attach(filename=os.path.basename('../../'+filename), content_type='text/csv',data=file.read())
        
        with app.open_resource('../../'+filename) as file:
            msg.attach(filename=os.path.basename('../../'+filename),
                    content_type='text/csv',
                    data=file.read())
        mail.send(msg)
        return {
                 "success": "true",
                 "msg": "File sent to mail"
            }
    except Exception as e:
        print("cele",e)
        return {
                "success":"false",
                "msg":"Invalid server Error",
                "error":str(e)
        }   


@shared_task(ignore_result=False)
def alert_user():
    try:
        app = create_app()
        bookings = Booking.query.filter(Booking.booked_date == datetime.date.today()).all() 
        users = User.query.all()
        booked_users = []
        for b in bookings:
            if b.user_id not in booked_users:
                booked_users.append(b.user_id)
        recipient_list = [] 
        for u in users:
            if u.email not in booked_users and u.role!="admin":
                recipient_list.append(u.email)
        subject = f"Book your tickets and watch the latest movies"
        body = f"===TicketShow===\n\nWatch out the latest movies from the theatres near you.\n\nSeats filling fast!!\nGet your tickets soon."
        msg = Message(subject=subject,
                    sender="22f2001140@ds.study.iitm.ac.in",
                    recipients=recipient_list)
        msg.body = body
        mail.send(msg)
        return {
                    "success": "true",
                    "ready": "true",
                    "msg": "Notified users"
                }
    except Exception as e:
        print(e)
        return {
                    "success": "false",
                    "ready": "true",
                    "msg": "Error in Notifying users"
                }
    
@shared_task(ignore_result=False)
def monthly_report():
    try:
        app = create_app()
        current_date = datetime.datetime.now()
        
        
        first_day_of_previous_month = current_date.replace(day=1) - datetime.timedelta(days=1)
        first_day_of_previous_month = first_day_of_previous_month.replace(day=1)
        last_day_of_previous_month = first_day_of_previous_month.replace(day=1) - datetime.timedelta(days=1)

        users = User.query.all()
        for u in users:
            bookings = Booking.query.filter(
                        Booking.user_id == u.id,
                        Booking.booked_date >= first_day_of_previous_month.date(),
                        Booking.booked_date <= last_day_of_previous_month.date()
                    ).all()
            table_rows = []
            for b in bookings:
                movie = Movie.query.filter(Movie.id == b.movie_id).first()
                theatre = Theatre.query.filter(Theatre.id == b.theatre_id).first()
                slot = Slot.query.filter(Slot.id == b.slot_id).first()
                row = {
                    'movie_name': movie.title,
                    'theatre_name': theatre.name,
                    'slot_date': str(slot.date),
                    'slot_time': str(slot.time),
                    'seat_count': b.no.of.tickets,
                    'user_rating': b.user_rating,
                    'cost': b.cost,
                    'booking_date': str(b.booked_date),
                }
                table_rows.append(row)
            subject = f"Report for {first_day_of_previous_month.date()}-{last_day_of_previous_month.date()}"


            msg = Message(subject=subject,
                        sender="22f2001140@ds.study.iitm.ac.in",
                        recipients=[u.email])
            
            rendered_html = render_template_string('''<html>
                        <body>
                            <h1>TicketShow</h1>
                            <h3>Hello {{ username }}, Your Bookings for the last month</h3>
                            <h4>Monthly report {{ first_date }} - {{ last_date }}</h4>
                        <table border="1">
                            <tr>
                                <th>Movie Name</th>
                                <th>Date</th>
                                <th>Time</th>
                                <th>No. of Tickets</th>
                                <th>Cost</th>
                                <th>Rating</th>
                                <th>Theatre Name</th>
                                <th>Booking Date</th>
                                <th>Booking Time</th>
                            </tr>
                            {% if table_rows != [] %}
                            {% for row in table_rows %}
                            <tr>
                                <td>{{ row.movie_name }}</td>
                                <td>{{ row.slot_date }}</td>
                                <td>{{ row.slot_time }}</td>
                                <td>{{ row.seat_count }}</td>
                                <td>{{ row.cost }}</td>
                                <td>{{ row.user_rating }}</td>
                                <td>{{ row.venue_name }}</td>
                                <td>{{ row.booked_date }}</td>
                            </tr>
                            {% endfor %}
                            {% else %}
                            <tr>
                                <td colspan="9">No Bookings</td>
                            </tr>
                            {% endif %}
                        </table> 
                        </body>
                    </html>''',
                    table_rows = table_rows,
                    first_date = first_day_of_previous_month.date(),
                    last_date = last_day_of_previous_month.date(),    
                    username = u.username         
                )

            msg.html = rendered_html
            mail.send(msg)
        return {
                "success": "true",
                "ready": "true",
                "msg": "Monthly Report Published"
            }
    except Exception as e:
        print(e)
        return {
                "success": "false",
                "ready": "true",
                "msg": "Error in publishing monthly report"
            }
    