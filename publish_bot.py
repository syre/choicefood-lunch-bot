#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import (
	Flask,
	jsonify,
)
import json

import lunch_scraper

app = Flask(__name__)

@app.route("/lunch", methods=["GET", "POST"])
def get_lunch():
	output = lunch_scraper.get_menu_output()
	return jsonify(
		{
			"response_type": "in_channel",
			"text": "Todays lunch menu is:",
			"attachments": [{"text": output}]
		}
	)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5050)
