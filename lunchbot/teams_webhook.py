#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script should run hourly.

If the email message is received within the previous hour we can send
the payload, alternatively if it's currently 7:00 we send the payload.

Eg. email received 6:00, script runs at 7:00 and does not send the payload.
    email received 6:00, script runs at 8:00 and does not send the payload.
    email received yesterday at 7:00, script runs at 7:00, sends the payload.
"""
import sys
from datetime import datetime

import requests

from utils import (
    is_in_previous_hour,
    is_seven_o_clock_danish_time,
    remove_excessive_newlines,
)
from lunch_scraper import (
    get_menu_output,
    get_messages,
    extract_email_time,
    extract_link_from_message
)
from settings import TEAMS_WEB_HOOK_POST_URL

if __name__ == '__main__':
    now = datetime.now()
    messages = get_messages()
    if not messages:
        sys.exit()
    # We assume there is only one message.
    message = messages[0]
    menu_link = extract_link_from_message(message)
    email_time = extract_email_time(message)
    send_message = (is_in_previous_hour(email_time) or
                    is_seven_o_clock_danish_time(now))
    output = get_menu_output()
    formatted_output = remove_excessive_newlines(output)

    if send_message:
        print("sending message!")
        requests.post(
            TEAMS_WEB_HOOK_POST_URL,
            json={
                "title": "Today's menu",
                "text": "[menu link]({})\n\n{}".format(
                    menu_link,
                    formatted_output
                )
            }
        )
    else:
        print("time is not right yet!")
