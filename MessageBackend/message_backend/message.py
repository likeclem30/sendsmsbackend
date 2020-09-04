import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

accountSid = os.environ.get('ACCOUNT_SID',
                            'ACa0cd653665eb1e653089c2133df90581')
authToken = os.environ.get('AUTH_TOKEN',
                           '8430da1915608e1ea6f0c6a087799fc9')
fromNo = 'Zeno'
CALLBACK = os.environ.get('CALL_BACK',
                          'http://34.209.29.96:7001/api/status/')


client = Client(accountSid, authToken)


def send_message(body, to):
    try:
        message = client.messages \
                        .create(
                            body=body,
                            from_=fromNo,
                            status_callback=CALLBACK,
                            to=to
                        )

    except TwilioRestException:
        print('came here')
        return {'sent': False}

    return {'sent': True, 'response': message}
