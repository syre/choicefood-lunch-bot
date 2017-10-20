#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import lunch_scraper

WEB_HOOK_POST_URL = "https://outlook.office.com/webhook/e55cb28b-1ec8-4c13-89a9-66e69637a54d@e62d78b0-89a4-4d47-81c0-03d7b05d12f1/IncomingWebhook/e3f13eca6ed844e1b43f58a27d1f1515/0106ec0d-7bf2-46d9-8192-7408b6d52db3"

output = lunch_scraper.get_menu_output()
requests.post(WEB_HOOK_POST_URL, json={"title": "Today's menu", "text": output})
