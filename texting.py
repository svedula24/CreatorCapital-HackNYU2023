# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

def introText(number):
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                         body="Log on to Creator Capital",
                         from_='+16262381040',
                         to=number
                     )

    print(message.sid)
