import time
import booking
import datetime
import court5
import court8
import logging
from helper import store_booking, send_court_alert




# TODO:
# - Remote service pause and resume
# - Store each user's booking list in separate files/db tables
    # + modify send_court_alert to send alerts to each user based on their booking list"
def main():
    while True:    
        logging.basicConfig(filename="scraper.log", format='%(asctime)s %(message)s', filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        store_booking(booking.Booking(0, datetime.datetime(2021, 10, 10, 10, 10)))


        logger.info(f"---------{datetime.datetime.now().strftime('%d/%m/%Y   %H:%M:%S')}---------")
        logger.info("Starting alert service...")
        logger.info("Searching available slots for Court 5...")
        court5.court5()
        logger.info("Searching available slots for Court 8...")
        court8.court8()
        logger.info("Sending court alert... (if any new bookings are available)")
        send_court_alert()
        logger.info("Waiting for 1 hour...")
        time.sleep(3600)
        
if __name__ == "__main__":
    main()