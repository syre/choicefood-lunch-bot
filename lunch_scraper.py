#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re
import subprocess
import tempfile
import shutil

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

WEEK_PATTERN = "Uge {}"

# If it's friday make the end index "velbekomme"
if NOW.weekday() == 4:
    WEEK_PATTERN = WEEK_PATTERN.format(NOW.isocalendar()[1])
    START_INDEX = WEEKDAY_DICT[NOW.weekday()]
    END_INDEX = "velbekomme"
# If it's weekend let's take mondays menu
if NOW.weekday() > 4:
    WEEK_PATTERN = WEEK_PATTERN.format(NOW.isocalendar()[1]+1)
    START_INDEX = WEEKDAY_DICT[0]
    END_INDEX = WEEKDAY_DICT[1]
else:
    WEEK_PATTERN = WEEK_PATTERN.format(NOW.isocalendar()[1])
    START_INDEX = WEEKDAY_DICT[NOW.weekday()]
    END_INDEX = WEEKDAY_DICT[NOW.weekday()+1]

def get_menu_output():
    # Grab current weeks PDF menu.
    elem = soup.find("strong", text=re.compile(WEEK_PATTERN))
    pdf_url = "{}{}".format(ROOT_URL, elem.parent.parent.a["href"])

    response = requests.get(pdf_url, stream=True)
    # Save the menu to a file and run pdftotext on it.
    with tempfile.NamedTemporaryFile() as file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
        output = subprocess.check_output(["pdftotext", file.name, "-"]).lower().decode("utf-8")

    RE_STRING = r"({}.*?){}".format(START_INDEX, END_INDEX)

    regex_object = re.compile(RE_STRING, re.DOTALL)
    menu_output = re.search(regex_object, output).group(1)
    return menu_output

if __name__ == '__main__':
    print(get_menu_output())