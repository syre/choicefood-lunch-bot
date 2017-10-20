#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import lunch_scraper

WEB_HOOK_POST_URL = "https://saxo.ryver.com/application/webhook/Tz2BoOfe64VhDxY"

output = lunch_scraper.get_menu_output()

requests.post(WEB_HOOK_POST_URL, json={"body": output})
