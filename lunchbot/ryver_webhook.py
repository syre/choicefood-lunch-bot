#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import requests

from utils import (
    is_in_previous_hour,
    is_seven_o_clock_danish_time,
    remove_excessive_spacing,
)
from lunch_scraper import (
    get_menu_output,
    get_messages,
    extract_email_time,
    extract_link_from_message
)
from settings import RYVER_WEB_HOOK_POST_URL

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
    formatted_output = remove_excessive_spacing(output)

    if send_message:
        requests.post(RYVER_WEB_HOOK_POST_URL, json={"body": formatted_output})
    else:
        print("time is not right yet!")
