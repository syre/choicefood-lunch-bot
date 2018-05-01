#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re
import subprocess
import os
import base64

import googleapiclient
import requests
import bs4

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
STORE = file.Storage('credentials.json')
CREDS = STORE.get()
if not CREDS or CREDS.invalid:
    FLOW = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    CREDS = tools.run_flow(FLOW, STORE)

SERVICE = build('gmail', 'v1', http=CREDS.authorize(Http()))

"""
Menu setup is like this:

Monday    Tuesday
Wednesday Thursday
Friday

"""
WEEKDAY_MENU_INDEXES_DICT = {
    0: ("mandag", "onsdag"),
    1: ("tirsdag", "torsdag"),
    2: ("onsdag", "fredag"),
    # Thursday is last in column 2 so end index is the right column footer.
    3: ("torsdag", "velbekomme"),
    # Friday is last in column 1 so end index is the left column footer.
    4: ("fredag", "www.choicefood.dk")
}


def get_week_pattern():
    week_pattern = "uge {}"
    now = datetime.now()
    # If it's weekend, get next week.
    if now.weekday() > 4:
        week_pattern = week_pattern.format(now.isocalendar()[1] + 1)
    else:
        week_pattern = week_pattern.format(now.isocalendar()[1])
    return week_pattern


def get_pdf_indexes(weekday):
    # Get column.
    column_index = 0 if weekday % 2 == 0 else 1
    # If it's weekend let's take mondays menu.
    if weekday > 4:
        return column_index, (*WEEKDAY_MENU_INDEXES_DICT[0])
    else:
        return column_index, (*WEEKDAY_MENU_INDEXES_DICT[weekday])

def extract_link_from_message_body(body):
    week_pattern = get_week_pattern()
    soup = bs4.BeautifulSoup(body, "html.parser")
    element = soup.find("a", text=re.compile(week_pattern))
    if element:
        return element["href"]
    return None

def get_lunch_message_bodies():
    """
    Retrieve message bodies from Gmail with lunch bot label.
    """
    week_pattern = get_week_pattern()

    label_name = "SaxoLunchBot"

    label_results = SERVICE.users().labels().list(userId='me').execute()
    labels = [label for label in label_results["labels"] if label["name"] == label_name]
    if not labels:
        raise Exception("Lunch Bot label could not be found")
    label = labels[0]
    # Get all messages with lunch bot label.
    messages_results = SERVICE.users().messages().list(
        userId="me",
        labelIds=[label["id"]],
        q="Frokostmenu {}".format(week_pattern)
    ).execute()
    # For each message get the body.
    message_bodies = []
    for message in messages_results["messages"]:
        message_result = SERVICE.users().messages().get(userId="me", id=message["id"], metadataHeaders=["body"]).execute()
        html_parts = [part for part in message_result["payload"]["parts"] if part["mimeType"] == "text/html"]
        email_body = base64.urlsafe_b64decode(html_parts[0]["body"]["data"])
        message_bodies.append(email_body)
    return message_bodies

def extract_pdf_output(weekday):
    # Grab current weeks PDF menu link.
    message_bodies = get_lunch_message_bodies()
    menu_link = None
    for body in message_bodies:
        link = extract_link_from_message_body(body)
        if link:
            menu_link = link
        break
    if not menu_link:
        raise Exception("Lunch menu link could not be found")

    response = requests.get(menu_link, stream=True)
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
        left_column_output = subprocess.check_output(
            ["pdftotext", "-layout", "-x", "0", "-y", "110", "-W", "300", "-H", "1000", filename, "-"]
        ).lower().decode("utf-8")
        right_column_output = subprocess.check_output(
            ["pdftotext", "-layout", "-x","300", "-y", "110", "-W", "300", "-H", "1000", filename, "-"]
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

    return (left_column_output, right_column_output)

def add_formatting(output):
    output = re.sub(r"\n{1,}", "\n\n", output)
    output = re.sub(r" {2}", "&nbsp;", output)
    return output

def get_menu_output():
    weekday = datetime.now().weekday()
    column_tuple = extract_pdf_output(weekday)
    column_index, start_index, end_index = get_pdf_indexes(weekday)
    regex_string = r"({}.*?){}".format(start_index, end_index)

    regex_object = re.compile(regex_string, re.DOTALL)
    menu_output = re.search(regex_object, column_tuple[column_index]).group(1)
    menu_output = add_formatting(menu_output)
    return menu_output


if __name__ == '__main__':
    print(get_menu_output())

