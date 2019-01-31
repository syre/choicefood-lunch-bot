[![pipeline status](https://gitlab.com/syre/choicefood-lunch-bot/badges/master/pipeline.svg)](https://gitlab.com/syre/choicefood-lunch-bot/commits/master)
# Choicefood.dk LunchBot

This is the official (not really) LunchBot for scraping menu emails received from the caterer [Choicefood.dk](https://choicefood.dk/) from a Mail supporting IMAP and posting them to your chat client of choice ([Microsoft Teams](http://teams.microsoft.com/) and [Ryver](https://ryver.com/) right now).
# Demo

Example LunchBot output

![Example LunchBot output](https://gitlab.com/syre/choicefood-lunch-bot/raw/master/examples/lunchbot_example.gif)

Example Teams Webhook output

![Example Teams Webhook output](https://gitlab.com/syre/choicefood-lunch-bot/raw/master/examples/teams_webhook_example.png?raw=true)

# Requirements
* python requirements defined in the `requirements.txt`
* `pdftotext` from `poppler-utils`

# Installation

As the mighty chef Ronnie from Choicefood.dk only shares his menu with his most intimate of friends through email, the requirements right now are a bit intricate.

1. get on the mailing list (good luck)
2. label all incoming mail from email@choicefood.dk with a label name of your choice and set up a web hook in your chat client of choice
3. input the web hook url, the email label name, the email imap host and port into the sample `settings.py` file
4. set the environmental variables `MAIL_USER` and `MAIL_PASS` in the running environment corresponding to your IMAP username and password
5. run `python -m lunchbot.lunch_scraper`
6. ??
7. profit!