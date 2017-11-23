#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import lunch_scraper

WEB_HOOK_POST_URL = "https://outlook.office.com/webhook/866381db-7215-4044-ab9f-f391ea683a74@***REMOVED***/IncomingWebhook/1daa413023754b02b1744faa1893b7eb/***REMOVED***"

output = lunch_scraper.get_menu_output()
requests.post(WEB_HOOK_POST_URL, json={"title": "Today's menu", "text": output})
