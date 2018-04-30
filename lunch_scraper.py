#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re
import subprocess
import os
import googleapiclient
import requests
import bs4

WEEKDAY_DICT = {
    0: "mandag",
    1: "tirsdag",
    2: "onsdag",
    3: "torsdag",
    4: "fredag",
    5: "lørdag",
    6: "søndag"
}

MENU_URL = "http://www.dg-mad.dk/Frokostordning/Menuoversigt.html"

ROOT_URL = "http://www.dg-mad.dk"


def get_week_pattern():
    week_pattern = "Uge {}"
    now = datetime.now()
    # If it's weekend, get next week.
    if now.weekday() > 4:
        week_pattern = week_pattern.format(now.isocalendar()[1] + 1)
    else:
        week_pattern = week_pattern.format(now.isocalendar()[1])
    return week_pattern


def get_pdf_indexes():
    now = datetime.now()
    # If it's friday make the end index "velbekomme".
    if now.weekday() == 4:
        start_index = WEEKDAY_DICT[now.weekday()]
        end_index = "velbekomme"
    # If it's weekend let's take mondays menu.
    elif now.weekday() > 4:
        start_index = WEEKDAY_DICT[0]
        end_index = WEEKDAY_DICT[1]
    else:
        start_index = WEEKDAY_DICT[now.weekday()]
        end_index = WEEKDAY_DICT[now.weekday()+1]
    return start_index, end_index


def get_emails():
    """
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    """
    # client secret icGoKFxoerjEV-GOl3qsCHbZ
    # client id 60930985587-tjl4soqpjl1qqe5ideet1shooik4lp55.apps.googleusercontent.com
    gmail_service = build('gmail', 'v1', developerKey=api_key)
    print(gmail_service.users.settings.getImap("me"))


def extract_pdf_output():
    week_pattern = get_week_pattern()

    response = requests.get(MENU_URL)

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Grab current weeks PDF menu.
    elem = soup.find("strong", text=re.compile(week_pattern))
    if not elem:
        elem = soup.find(text=re.compile(week_pattern)).find_next_sibling()
    pdf_url = "{}{}".format(ROOT_URL, elem.parent.a["href"])

    response = requests.get(pdf_url, stream=True)
    # Save the menu to a file and run pdftotext on it.
    if response.status_code != 200:
        raise RuntimeError(
            "unsuccessful response for getting the menu: {}".format(
                response.status_code
            )
        )
    filename = "menu.pdf"
    with open(filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    try:
        output = subprocess.check_output(
            ["pdftotext", filename, "-"]
        ).lower().decode("utf-8")
    except subprocess.CalledProcessError as exception:
        raise RuntimeError(
            "command '{}' return with error (code {}): {}".format(
                exception.cmd,
                exception.returncode,
                exception.output
            )
        )
    finally:
        os.remove(filename)

    return output


def add_formatting(output):
    output = output.replace("\n", "\n\n")
    output = output.replace("•", "-")
    return output


def get_menu_output():
    output = extract_pdf_output()
    start_index, end_index = get_pdf_indexes()

    regex_string = r"({}.*?){}".format(start_index, end_index)

    regex_object = re.compile(regex_string, re.DOTALL)
    menu_output = re.search(regex_object, output).group(1)
    menu_output = add_formatting(menu_output)
    return menu_output


if __name__ == '__main__':
    print(get_emails())
