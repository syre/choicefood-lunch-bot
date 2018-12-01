[![pipeline status](https://gitlab.com/syre/choicefood-lunch-bot/badges/master/pipeline.svg)](https://gitlab.com/syre/choicefood-lunch-bot/commits/master)
# Choicefood.dk LunchBot

This is the official (not really) LunchBot for scraping menu emails received from the caterer [Choicefood.dk](https://choicefood.dk/) from a [Gmail account](http://gmail.com/) and posting them to your chat client of choice ([Microsoft Teams](http://teams.microsoft.com/) and [Ryver](https://ryver.com/) right now).
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
3. input the web hook url and the email label name into the sample `settings.py` file
4. get a `client_secret.json` Oauth 2.0 file file from your [Google Developer Console](https://console.developers.google.com/apis/credentials?pli=1) allowing you to access the Gmail API and place it in the root folder
5. run `lunch_scraper.py` and allow it to generate a `credentials.json` with the Gmail API
6. ??
7. profit!