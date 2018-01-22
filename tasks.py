#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from microsoftbotframework import ReplyToActivity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import lunch_scraper
from models import *

engine = create_engine("sqlite:///lunch.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def echo_response(message):
    if message["type"] == "message":
        print(message)
        ReplyToActivity(fill=message, text=message["text"]).send()

def fetch_lunch_response(message):
	menu_output = lunch_scraper.get_menu_output()
	lunch_string = "**Today's Menu**\n\n{}".format(menu_output)
	today = datetime.now().date()

	todays_menu = session.query(LunchMenu).filter_by(date=today).first()
	if not todays_menu:
		todays_menu = LunchMenu(description=menu_output, date=today)
		session.add(todays_menu)
		session.commit()

	if message["type"] == "message" and message["text"] == "/lunch":
		ReplyToActivity(fill=message, textFormat="markdown", text=lunch_string).send()

def rate_lunch_response(message):
	today = datetime.now().date()
	todays_menu = session.query(LunchMenu).filter_by(date=today).first()
	if not todays_menu:
		todays_menu = LunchMenu(description=menu_output, date=today)
		session.add(todays_menu)
		session.commit()

	if message["type"] == "message" and message["text"].startswith("/rate"):
		# Do the rating processing
		text = message["text"].replace("/rate", "")
		try:
			rating = int(text)
			chat_id = message["from"]["id"]
			name = message["from"]["name"]
			user = session.query(User).filter_by(chat_id=chat_id).first()
			if not user:
				user = User(name=name, chat_id=chat_id)
				session.add(user)
				session.commit()
			if session.query(LunchRating).filter_by(user_id=user.id, lunchmenu_id=todays_menu.id).first():
				ReplyToActivity(fill=message, text="You already rated today's lunch").send()
				return
			else:
				session.add(LunchRating(rating=rating, user_id=user.id, lunchmenu_id=todays_menu.id))
				session.commit()
				ReplyToActivity(fill=message, text="You rated today's lunch {}".format(rating)).send()
		except:
			ReplyToActivity(fill=message, text="LunchBot could not understand you").send()
