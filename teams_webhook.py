#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import lunch_scraper

WEB_HOOK_POST_URL = "https://outlook.office.com/webhook/e55cb28b-1ec8-4c13-89a9-66e69637a54d@***REMOVED***/IncomingWebhook/e3f13eca6ed844e1b43f58a27d1f1515/***REMOVED***"

output = lunch_scraper.get_menu_output()
requests.post(WEB_HOOK_POST_URL, json={"title": "Today's menu", "text": output})
