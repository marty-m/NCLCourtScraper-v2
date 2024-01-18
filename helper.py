import os
from dotenv import load_dotenv
from twilio.rest import Client



load_dotenv()


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")


TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

twilioClient = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_message(destinationNr, message):
    twilioClient.api.account.messages.create(
                    to=destinationNr,
                    from_="+447700142025",
                    body=message)
