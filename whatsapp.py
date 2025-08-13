# whatsapp.py
import os
from twilio.rest import Client

TW_SID = os.getenv("TWILIO_SID")
TW_TOKEN = os.getenv("TWILIO_TOKEN")
TW_FROM = os.getenv("TWILIO_WHATSAPP_FROM")  # e.g. 'whatsapp:+1415xxxx'

def send_whatsapp(to_number, message):
    if not (TW_SID and TW_TOKEN and TW_FROM):
        raise RuntimeError("Twilio creds not set")
    client = Client(TW_SID, TW_TOKEN)
    msg = client.messages.create(body=message, from_=TW_FROM, to=f'whatsapp:{to_number}')
    return msg.sid
