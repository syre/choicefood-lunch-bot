#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re
import subprocess
import tempfile

import requests
import bs4

NOW = datetime.now()

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

response = requests.get(MENU_URL)

soup = bs4.BeautifulSoup(response.text, "html.parser")

WEEK_PATTERN = "Uge {}".format(NOW.isocalendar()[1])

def get_menu_output():
    # Grab current weeks PDF menu.
    for elem in soup(text=re.compile(WEEK_PATTERN)):
        pdf_url = "{}{}".format(ROOT_URL, elem.parent.parent.a["href"])

    response = requests.get(pdf_url, stream=True)

    # Save the menu to a file and run pdftotext on it.
    with tempfile.NamedTemporaryFile() as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
        output = subprocess.check_output(["pdftotext", file.name, "-"]).lower().decode("utf-8")

    # TODAYS_WEEKDAY = WEEKDAY_DICT[NOW.weekday()]
    # TOMORROWS_WEEKDAY = WEEKDAY_DICT[NOW.weekday()+1]
    TODAYS_WEEKDAY = "tirsdag"
    TOMORROWS_WEEKDAY = "onsdag"
    RE_STRING = r"({}.*?){}".format(TODAYS_WEEKDAY, TOMORROWS_WEEKDAY)

    regex_object = re.compile(RE_STRING, re.DOTALL)
    menu_output = re.search(regex_object, output).group(1)
    return menu_output
