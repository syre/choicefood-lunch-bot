#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import (
	Flask,
	jsonify,
)
from flask_sqlalchemy import SQLAlchemy
import json

import lunch_scraper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://lunch.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), unique=True, nullable=False)
    email = db.Column(db.Text(), unique=True, nullable=False)
    ratings = db.relationship('LunchRating', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class LunchMenu(db.Model):
	description = db.Column(db.Text(), nullable=False)
	date = db.Column(db.Date(), nullable=False)

class LunchRating(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
	rating_value = db.Column(db.Integer, nullable=False)


@app.route("/lunch/rate", methods=["POST"])
def post_lunch_rating():
	if request.method == "POST":
		json_post = request.get_json()


	response = jsonify(
		{
			"response_type": "in_channel",
			"text": "Todays lunch menu is:",
			"attachments": [{"text": output}]
		}
	)
	response.headers["CARD-ACTION-STATUS"] = "Rating submitted"
	response.headers["CARD-UPDATE-IN-BODY"] = True

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5050)
