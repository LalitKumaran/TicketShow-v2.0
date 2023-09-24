from celery import shared_task
from flask import render_template_string
import csv,os
from flask_mail import Message
from . import db,mail,app,cel_app,createapp
from .models import Booking,User,Show,Venue,Slot
import datetime


@shared_task(ignore_result=False)
def export_csv_to_user(csv_filename,user,venue):
    try:
        app = createapp()
        subject = f"CSV Report for {venue['venue_name']}"
        body = f"Please find the CSV file attached for the Venue {venue['venue_name']} located at {venue['location']} with a capacity of {venue['capacity']}"
        msg = Message(subject=subject,
                    sender=os.environ.get('MAIL_USERNAME'),
                    recipients=[user['email']])
        msg.body = body
        with app.open_resource('../../'+csv_filename) as file:
            msg.attach(filename=os.path.basename('../../'+csv_filename),
                    content_type='text/csv',
                    data=file.read())
        mail.send(msg)
        return {
                 "success": "true",
                 "ready": "true",
                 "msg": "File sent to mail"
            }
    except Exception as e:
        print(e)
        return {
                "success":"false",
                "ready": "true",
                "msg":"Invalid server Error"
            }
    
@shared_task(ignore_result=False)
def alert_user():
    try:
        app = createapp()
        bookings = Booking.query.filter(Booking.booking_date == datetime.date.today()).all() 
        users = User.query.all()
        booked_users = []
        for b in bookings:
            if b.user_id not in booked_users:
                booked_users.append(b.user_id)
        recipient_list = [] 
        for u in users:
            if u.email not in booked_users and u.role!="admin":
                recipient_list.append(u.email)
        subject = f"Grab your tickets for the latest shows"
        body = f"---TicketShow---\n\nWatch out the latest movies from the theatres near you.\n\nSeats filling fast!!\nGrab your seats soon."
        msg = Message(subject=subject,
                    sender=os.environ.get('MAIL_USERNAME'),
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
        app = createapp()
        current_date = datetime.datetime.now()
        
        
        # first_day_of_previous_month = current_date.replace(day=1)
        # last_day_of_previous_month = datetime.datetime(current_date.year,current_date.month+1,1) - datetime.timedelta(days=1)
        
        first_day_of_previous_month = current_date.replace(day=1) - datetime.timedelta(days=1)
        first_day_of_previous_month = first_day_of_previous_month.replace(day=1)
        last_day_of_previous_month = first_day_of_previous_month.replace(day=1) - datetime.timedelta(days=1)

        # print(first_day_of_previous_month.date())
        # print(last_day_of_previous_month.date())
        users = User.query.all()
        for u in users:
            bookings = Booking.query.filter(
                        Booking.user_id == u.user_id,
                        Booking.booking_date >= first_day_of_previous_month.date(),
                        Booking.booking_date <= last_day_of_previous_month.date()
                    ).all()
            table_rows = []
            for b in bookings:
                show = Show.query.get(b.show_id)
                venue = Venue.query.get(b.venue_id)
                slot = Slot.query.get(b.slot_id)
                row = {
                    'show_name': show.show_name,
                    'venue_name': venue.venue_name,
                    'slot_date': str(b.date),
                    'slot_time': str(b.time),
                    'seat_count': b.seat_count,
                    'user_rating': b.user_rating,
                    'amount': b.amount,
                    'booking_date': str(b.booking_date),
                    'booking_time' : (b.booking_time).strftime('%H:%M:%S')
                }
                table_rows.append(row)
            subject = f"Entertainment report for {first_day_of_previous_month.date()}-{last_day_of_previous_month.date()}"


            msg = Message(subject=subject,
                        sender=os.environ.get('MAIL_USERNAME'),
                        recipients=[u.email])
            
            rendered_html = render_template_string('''<html>
                        <body>
                            <h1>TicketShow</h1>
                            <h3>Hello {{ username }}, Your Bookings for the last month</h3>
                            <h4>Monthly report {{ first_date }} - {{ last_date }}</h4>
                        <table border="1">
                            <tr>
                                <th>Show Name</th>
                                <th>Date</th>
                                <th>Time</th>
                                <th>Seats booked</th>
                                <th>Amount</th>
                                <th>Rating</th>
                                <th>Venue Name</th>
                                <th>Booking Date</th>
                                <th>Booking Time</th>
                            </tr>
                            {% if table_rows != [] %}
                            {% for row in table_rows %}
                            <tr>
                                <td>{{ row.show_name }}</td>
                                <td>{{ row.slot_date }}</td>
                                <td>{{ row.slot_time }}</td>
                                <td>{{ row.seat_count }}</td>
                                <td>{{ row.amount }}</td>
                                <td>{{ row.user_rating }}</td>
                                <td>{{ row.venue_name }}</td>
                                <td>{{ row.booking_date }}</td>
                                <td>{{ row.booking_time }}</td>
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
    

