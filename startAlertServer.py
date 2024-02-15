import time
import booking
import datetime
import court5
import court8
from helper import store_booking, send_court_alert




# TODO:
# - Remote service pause and resume
def main():
    store_booking(booking.Booking(0, datetime.datetime(2021, 10, 10, 10, 10)))
    while True:
        print(f"---------{datetime.datetime.now().strftime('%d/%m/%Y   %H:%M:%S')}---------")
        print("Starting alert service...")
        print("Searching available slots for Court 5...")
        court5.court5()
        print("Searching available slots for Court 8...")
        court8.court8()
        print("Sending court alert... (if any new bookings are available)")
        send_court_alert()
        print("Waiting for 2 hours...")
        time.sleep(7200)

if __name__ == "__main__":
    main()