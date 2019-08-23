import logging
from twilio.rest import Client
import azure.functions as func
import os


account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio = Client(account_sid, auth_token)
twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
my_phone = os.getenv('MY_PHONE_NUMBER')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        resp = twilio.messages.create(
            to=my_phone,
            from_=twilio_phone,
            body="Hi there! {}".format(name)
        )
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
