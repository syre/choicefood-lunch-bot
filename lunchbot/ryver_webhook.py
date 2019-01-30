#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import requests

from lunchbot.utils import (
    is_in_previous_hour,
    is_seven_o_clock_danish_time,
    add_formatting,
    convert_unix_time_in_ms_to_datetime,
)
from lunchbot.lunch_scraper import (
    get_menu_output,
    get_messages,
    extract_link_from_message,
)
from lunchbot.settings import RYVER_WEB_HOOK_POST_URL

if __name__ == '__main__':
    now = datetime.now()
    messages = get_messages()
    if not messages:
        sys.exit()
    # We assume there is only one message.
    message = messages[0]
    menu_link = extract_link_from_message(message, now)
    email_time = convert_unix_time_in_ms_to_datetime(message["internalDate"])
    send_message = (is_in_previous_hour(now, email_time) or
                    is_seven_o_clock_danish_time(now))
    output = get_menu_output()
    formatted_output = add_formatting(output)

    if send_message:
        requests.post(RYVER_WEB_HOOK_POST_URL, json={"body": formatted_output})
    else:
        print("time is not right yet!")
