# LunchBot

This is the official LunchBot for scraping menu emails received from the caterer https://choicefood.dk/ from a [Gmail account](http://gmail.com/) and posting them to your chat client of choice ([Microsoft Teams](http://teams.microsoft.com/) and [Ryver](https://ryver.com/) right now).
# Demo
![Example LunchBot output](https://gitlab.com/syre/choicefood-lunch-bot/raw/master/examples/lunchbot_example.gif)
![Example Teams Webhook output](https://gitlab.com/syre/choicefood-lunch-bot/raw/master/examples/teams_webhook_example.png?raw=true)

# Requirements
* python requirements defined in the `requirements.txt`
* `pdftotext` from `poppler-utils`

# Installation

As the mighty chef Ronnie from ChoiceFood.dk only shares his menu with his most intimate of friends through email, the requirements right now are a bit intricate.

1. label all incoming mail from email@choicefood.dk
2. input the web hook url from the chat client of your choice and the email label name into the sample `settings.py` file
4. get a `client_secret.json` file from Gmail allowing you to access the API and place it in the root folder
5. run `lunch_scraper.py` and allow it to generate a `credentials.json` with the Gmail API
6. ??
7. profit!