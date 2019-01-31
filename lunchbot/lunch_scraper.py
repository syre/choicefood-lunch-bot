#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import email
from email import policy
import imaplib
from datetime import datetime
import re
import subprocess
import os
import requests
import bs4


from lunchbot.exceptions import LunchBotException
from lunchbot.utils import (
    remove_excessive_newlines,
    get_earliest_weekday_date,
)

from lunchbot.settings import (
    EMAIL_LABEL,
    EMAIL_IMAP_HOST,
    EMAIL_IMAP_PORT,
)

# Retrieve the IMAP username and password from environmental variables.
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")

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
    """Get emails from IMAP client from lunch bot label inbox and from a given week."""
    messages = []
    imap = imaplib.IMAP4_SSL(EMAIL_IMAP_HOST, EMAIL_IMAP_PORT)
    imap.login(MAIL_USER, MAIL_PASS)
    imap.select(EMAIL_LABEL)
    earliest_weekday = get_earliest_weekday_date(week_datetime)
    criterion = 'SINCE "{}"'.format(earliest_weekday.strftime("%d-%b-%Y"))
    typ, data = imap.search("UTF-8", criterion)
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        message = email.message_from_bytes(data[0][1], policy=policy.default)
        messages.append(message)
    imap.close()
    imap.logout()

    return messages


def extract_email_body(message):
    """Find html parts of the email."""
    email_body = ""
    for part in message.walk():
        if part.get_content_type() == 'text/html':
            email_body = part.get_content()

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
    for message in messages:
        menu_link = extract_link_from_message(message, day_datetime)
        if menu_link:
            break
    if not menu_link:
        raise LunchBotException("Lunch menu link could not be found")
    # Extract the two text columns.
    text_columns = extract_pdf_text(menu_link)
    # Get the pdf indexes for the current weekday.
    column_index, start_index, end_index = get_pdf_indexes(
        day_datetime.weekday()
    )
    # Extract the weekday text separated by the indexes.
    regex_string = r"({}.*?){}".format(start_index, end_index)
    regex_object = re.compile(regex_string, re.DOTALL)
    menu_output = re.search(regex_object, text_columns[column_index]).group(1)

    formatted_menu_output = remove_excessive_newlines(menu_output)
    return formatted_menu_output


if __name__ == '__main__':
    print(get_menu_output())
