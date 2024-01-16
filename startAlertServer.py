import booking
import datetime

availableBookings: booking.Booking = []

def addBooking(booking: booking.Booking):
    for i in availableBookings:
        if i.dateTime == booking.dateTime and i.courtNr == booking.courtNr:
            return
    availableBookings.append(booking)
    print(availableBookings)

# TODO:
# - Twilio SMS alert to inform of cookie expiry with outlook verification number asking for approval
# - Twilio SMS alert to inform of new available booking 
# - Remote service pause and resume through Twilio SMS
def main():
    availableBookings.append(booking.Booking(0, datetime.datetime(2021, 10, 10, 10, 10), True))
    while True:
        return
    

