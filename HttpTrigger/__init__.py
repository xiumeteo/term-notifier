import logging
from twilio.rest import Client
import azure.functions as func
import os
import pyotp
import json

def str2bool(value): return {"True": True, "true": True}.get(value, False)

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio = Client(account_sid, auth_token)
twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
my_phone = os.getenv('MY_PHONE_NUMBER')
otp_key = os.getenv('OTP_KEY')
should_send_sms = str2bool(os.getenv('ENABLE_SMS'))
should_auth = str2bool(os.getenv('ENABLE_AUTH'))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    verifier = pyotp.TOTP(otp_key)
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Message and auth code are mandatory",
             status_code=400
        )
    else:
        message = req_body.get('message')
        code = req_body.get('code')

    if should_auth and not verifier.verify(code):
        return func.HttpResponse(
             "Auth code is wrong",
             status_code=401
        )

    if message:
        logging.info('Received message: {}'.format(message))
        if should_send_sms:
            resp = twilio.messages.create(
                to=my_phone,
                from_=twilio_phone,
                body=f"Completed! {message}"
            )
        return func.HttpResponse(
                body=json.dumps({'status':'OK', 'sent_sms':should_send_sms, 'used_auth':should_auth}), 
                status_code=201
            )
    else:
        return func.HttpResponse(
             status_code=400
        )
