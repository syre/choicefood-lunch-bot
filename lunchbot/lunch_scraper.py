#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re
import subprocess
import os
import base64

import requests
import bs4

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from exceptions import LunchBotException
from utils import remove_excessive_newlines
from settings import EMAIL_LABEL

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
STORE = file.Storage(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        'credentials.json'
    )
)
CREDS = STORE.get()
if not CREDS or CREDS.invalid:
    SECRET_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        'client_secret.json'
    )
    FLOW = client.flow_from_clientsecrets(SECRET_PATH, SCOPES)
    CREDS = tools.run_flow(FLOW, STORE)

SERVICE = build('gmail', 'v1', http=CREDS.authorize(Http()))

"""
Menu setup is like this (2 columns, 3 rows):

Monday    Tuesday
Wednesday Thursday
Friday

So we create a dict of weekday: (start_index, end_index) tuples
so we know where the menu for a given weekday starts and ends.
"""
WEEKDAY_MENU_INDEXES_DICT = {
    0: ("mandag", "onsdag"),
    1: ("tirsdag", "torsdag"),
    2: ("onsdag", "fredag"),
    # Thursday is last in column 1 so end index is the right column footer.
    3: ("torsdag", "velbekomme"),
    # Friday is last in column 0 so end index is the left column footer.
    4: ("fredag", "www.choicefood.dk")
}


def get_week_pattern(week_datetime=datetime.now()):
    """
    Get week pattern for a date for email searching.

    For example "uge 43".
    """
    week_pattern = "uge {}"
    # If it's weekend, get next week.
    if week_datetime.weekday() > 4:
        week_pattern = week_pattern.format(week_datetime.isocalendar()[1] + 1)
    else:
        week_pattern = week_pattern.format(week_datetime.isocalendar()[1])
    return week_pattern


def get_pdf_indexes(weekday):
    """
    Get the pdf column-, start- and end-indexes for a weekday.

    A monday would return 0, "mandag", "onsdag" as indexes.
    """
    # Get column.
    column_index = 0 if weekday % 2 == 0 else 1
    # If it's weekend let's take mondays menu.
    if weekday > 4:
        return column_index, (*WEEKDAY_MENU_INDEXES_DICT[0])
    return column_index, (*WEEKDAY_MENU_INDEXES_DICT[weekday])


def extract_link_from_message(message, week_datetime):
    """Extract the menu link from the message."""
    week_pattern = get_week_pattern(week_datetime)
    body = extract_email_body(message)
    soup = bs4.BeautifulSoup(body, "html.parser")
    element = soup.find("a", text=re.compile(week_pattern))
    if element:
        return element["href"]
    return None


def get_messages(week_datetime):
    """Get emails from Gmail with lunch bot label and from a given week."""
    week_pattern = get_week_pattern(week_datetime)

    label_results = SERVICE.users().labels().list(userId='me').execute()
    labels = [label for label in label_results["labels"] if label["name"] == EMAIL_LABEL]
    if not labels:
        raise LunchBotException("Lunch Bot label could not be found")
    label = labels[0]
    # Get all messages with lunch bot label.
    messages_results = SERVICE.users().messages().list(
        userId="me",
        labelIds=[label["id"]],
        q="Frokostmenu {}".format(week_pattern)
    ).execute()
    # Get all messages.
    messages = []
    if not "messages" in messages_results or not messages_results["messages"]:
        return []
    for message in messages_results["messages"]:
        message = SERVICE.users().messages().get(
            userId="me",
            id=message["id"],
            metadataHeaders=["body"]
        ).execute()
        messages.append(message)
    return messages


def extract_email_body(message):
    """Find html parts of the email, base64 decode the email body."""
    html_parts = [part for part in message["payload"]["parts"] if part["mimeType"] == "text/html"]
    email_body = base64.urlsafe_b64decode(html_parts[0]["body"]["data"])
    return email_body


def extract_pdf_text(menu_link):
    """Extract the pdf text for a menu with a link."""
    response = requests.get(menu_link, stream=True)
    # Save the menu to a file and run pdftotext on it.
    if response.status_code != 200:
        raise LunchBotException(
            "unsuccessful response for getting the menu: {}".format(
                response.status_code
            )
        )
    filename = "menu.pdf"
    with open(filename, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf_file.write(chunk)
    try:
        left_column_output = subprocess.check_output(
            ["pdftotext", "-layout", "-x", "0", "-y", "90", "-W", "300", "-H", "1000", filename, "-"]
        ).lower().decode("utf-8")
        right_column_output = subprocess.check_output(
            ["pdftotext", "-layout", "-x", "300", "-y", "90", "-W", "300", "-H", "1000", filename, "-"]
        ).lower().decode("utf-8")
    except subprocess.CalledProcessError as exception:
        raise LunchBotException(
            "command '{}' return with error (code {}): {}".format(
                exception.cmd,
                exception.returncode,
                exception.output
            )
        )
    finally:
        os.remove(filename)

    return (left_column_output, right_column_output)


def get_menu_output(day_datetime=datetime.now()):
    """Retrieve menu output for the current weekday."""
    messages = get_messages(day_datetime)
    if not messages:
        raise LunchBotException("Lunch message could not be found")
    # Grab current weeks PDF menu link.
    message = messages[0]
    menu_link = extract_link_from_message(message, day_datetime)
    if not menu_link:
        raise LunchBotException("Lunch menu link could not be found")
    # Extract the two text columns.
    text_columns = extract_pdf_text(menu_link)
    # Get the pdf indexes for the current weekday.
    column_index, start_index, end_index = get_pdf_indexes(day_datetime.weekday())
    # Extract the weekday text separated by the indexes.
    regex_string = r"({}.*?){}".format(start_index, end_index)
    regex_object = re.compile(regex_string, re.DOTALL)
    menu_output = re.search(regex_object, text_columns[column_index]).group(1)

    formatted_menu_output = remove_excessive_newlines(menu_output)
    return formatted_menu_output


if __name__ == '__main__':
    print(get_menu_output())
