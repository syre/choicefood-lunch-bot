#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script should run hourly.

If the email message is received within the previous hour we can send
the payload, alternatively if it's currently 7:00 we send the message.

Eg. email received 6:00, script runs at 7:00 and does not send the payload.
    email received 6:00, script runs at 8:00 and does not send the payload.
    email received yesterday at 7:00, script runs at 7:00, sends the payload.
"""
import sys
from datetime import (
    datetime,
    timedelta,
)

import requests
from pytz import timezone

from lunch_scraper import (
    get_menu_output,
    get_messages,
    extract_email_time,
    extract_link_from_message
)


def is_seven_o_clock_danish_time():
    """Check if datetime is seven o clock in the morning in Denmark."""
    now = datetime.now(
        tz=timezone("Europe/Copenhagen")
    )
    if now.hour == 7:
        return True
    return False


def is_in_previous_hour(email_datetime):
    """Check if datetime was in the previous hour."""
    now = datetime.now()
    previous_hour = (now - timedelta(hours=1)).replace(
        minute=0,
        second=0,
        microsecond=0
    )
    email_datetime_hour = email_datetime.replace(
        minute=0,
        second=0,
        microsecond=0
    )
    if previous_hour == email_datetime_hour:
        return True
    return False


WEB_HOOK_POST_URL = (
    "https://outlook.office.com/webhook/"
    "***REMOVED******REMOVED***/"
    "IncomingWebhook/***REMOVED***/"
    "***REMOVED***"
)
if __name__ == '__main__':
    messages = get_messages()
    if not messages:
        sys.exit()
    # We assume there is only one message
    message = messages[0]
    menu_link = extract_link_from_message(message)
    email_time = extract_email_time(message)
    send_message = (is_in_previous_hour(email_time) or
                    is_seven_o_clock_danish_time())
    output = get_menu_output()
    if send_message:
        print("sending message!")
        requests.post(
            WEB_HOOK_POST_URL,
            json={
                "title": "Today's menu",
                "text": "[menu link]({})\n\n{}".format(
                    menu_link,
                    output
                )
            }
        )
    else:
        print("time is not right yet!")
