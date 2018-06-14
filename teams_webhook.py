#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script should run hourly.

If the email message is received within the previous hour we can send the payload,
alternatively if it's currently 7:00 we send the message.

Eg. email received 6:00, the script runs at 7:00 and should send the payload there.
    email received 6:00, the script runs at 8:00 and should not send the payload.
    email received yesterday at 7:00, the script runs at 7:00 and sends the payload.
"""
import requests
from datetime import (
    datetime,
    timedelta,
)

from lunch_scraper import (
    get_menu_output,
    get_messages,
    extract_email_time,
)


def is_in_previous_hour_or_seven_o_clock(email_datetime):
    import pdb; pdb.set_trace()
    now = datetime.now()
    previous_hour = (datetime.now() - timedelta(hours=1)).replace(
        minute=0,
        second=0,
        microsecond=0
    )
    email_datetime_hour = email_datetime.replace(minute=0, second=0, microsecond=0)
    if previous_hour == email_datetime_hour or now.hour == 7:
        return True
    return False


WEB_HOOK_POST_URL = (
    "https://outlook.office.com/webhook/"
    "866381db-7215-4044-ab9f-f391ea683a74@***REMOVED***/"
    "IncomingWebhook/1daa413023754b02b1744faa1893b7eb/"
    "***REMOVED***"
)
messages = get_messages()
email_time = [extract_email_time(message) for message in messages][0]
send_message = is_in_previous_hour_or_seven_o_clock(email_time)
output = get_menu_output()
if send_message:
    print("sending message!")
    #requests.post(WEB_HOOK_POST_URL, json={"title": "Today's menu", "text": output})
else:
    print("time is not right yet!")
