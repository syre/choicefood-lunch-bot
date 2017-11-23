#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import lunch_scraper

WEB_HOOK_POST_URL = "***REMOVED***"

output = lunch_scraper.get_menu_output()
requests.post(WEB_HOOK_POST_URL, json={"title": "Today's menu", "text": output})
