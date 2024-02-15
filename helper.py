import datetime
import os
from dotenv import load_dotenv
from chump import Application
import json
import booking
import jsonpickle


load_dotenv()

PUSHOVER_APP_TOKEN= os.getenv("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_TOKEN = os.getenv("PUSHOVER_USER_TOKEN")

def send_message(title, message, priority=0):
    app = Application(PUSHOVER_APP_TOKEN)
    user = app.get_user(PUSHOVER_USER_TOKEN)
    user.send_message(title=title, message=message, priority=priority)

def send_court_alert():
    title = "New Court Booking(s) Available"
    message = "New bookings available:\n"

    availableBookings = get_stored_bookings()
    availableBookingsCopy = availableBookings.copy()

    for booking in availableBookings:
        if booking.dateTime < datetime.datetime.now():
            availableBookingsCopy.remove(booking)
        elif booking.dateTime > datetime.datetime.now() and not booking.alerted:
            message += f"Court {booking.courtNr} at {booking.dateTime.strftime('%d/%m/%Y %H:%M')}\n"
            booking.alerted = True
            availableBookingsCopy.append(booking)
        
    commit_booking_list(availableBookingsCopy)       
    if message != "New bookings available:\n":
        send_message(title, message)


def get_stored_cookie():
    if os.path.exists('cookie.json'):
        with open('cookie.json', 'r') as file:
            cookie = json.load(file)
    return cookie

def dump_cookie(cookie):
    with open('cookie.json', 'w') as file:
        json.dump(cookie, file)


def get_stored_bookings():
    if os.path.exists('bookings.json'):
        with open('bookings.json', 'r') as file:
            json_bookings = json.load(file)
        bookings = jsonpickle.decode(json_bookings)
    return bookings

def store_booking(booking: booking.Booking):
    availableBookings = get_stored_bookings()
    for i in availableBookings:
        if i.dateTime == booking.dateTime and i.courtNr == booking.courtNr:
            return
    availableBookings.append(booking)
    with open('bookings.json', 'w') as file:
        json_bookings = jsonpickle.encode(availableBookings)
        json.dump(json_bookings, file)

def commit_booking_list(bookingList):
    with open('bookings.json', 'w') as file:
        json_bookings = jsonpickle.encode(bookingList)
        json.dump(json_bookings, file)


