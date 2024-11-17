from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
import os
import requests
from requests.exceptions import ConnectionError, HTTPError


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):

    title = message[0]
    body= message[1]

    
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=title,
                        body=body,
                        sound='default',
                        data=extra))
    except PushServerError:
        # Encountered some likely formatting/validation error.
        print("Error sending push notification to client")

    except (ConnectionError, HTTPError):
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        print("Error sending push notification to client ")





