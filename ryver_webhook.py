#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import lunch_scraper

WEB_HOOK_POST_URL = (
    "https://saxo.ryver.com/application/"
    "webhook/***REMOVED***"
)

output = lunch_scraper.get_menu_output()
if __name__ == '__main__':
    messages = get_messages()
    if not messages:
        sys.exit()
    # We assume there is only one message.
    message = messages[0]
    menu_link = extract_link_from_message(message)
    email_time = extract_email_time(message)
    send_message = (is_in_previous_hour(email_time) or
                    is_seven_o_clock_danish_time())
    output = get_menu_output()

    if send_message:
        requests.post(WEB_HOOK_POST_URL, json={"body": output})
    else:
        print("time is not right yet!")
