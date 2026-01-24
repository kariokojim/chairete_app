import africastalking
from flask import current_app

def send_sms(phone, message):
    africastalking.initialize(
        current_app.config['AT_USERNAME'],
        current_app.config['AT_API_KEY']
    )
    africastalking.SMS._baseUrl = "http://api.sandbox.africastalking.com"

    sms = africastalking.SMS
    sms.send(message, [phone])
