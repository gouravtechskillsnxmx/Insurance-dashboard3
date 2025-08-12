from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()  # load from .env

TW_SID = os.getenv("TWILIO_SID")
TW_TOKEN = os.getenv("TWILIO_TOKEN")
TW_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

def send_whatsapp(to_number, message):
    if not (TW_SID and TW_TOKEN and TW_FROM):
        raise RuntimeError("Twilio credentials not set")
    client = Client(TW_SID, TW_TOKEN)
    msg = client.messages.create(body=message, from_=TW_FROM, to=f'whatsapp:{to_number}')
    return msg.sid
