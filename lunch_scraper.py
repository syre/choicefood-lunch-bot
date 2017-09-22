#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re
import subprocess
import tempfile
import shutil

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

def extract_pdf_output():
    week_pattern = get_week_pattern()    

    response = requests.get(MENU_URL)

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Grab current weeks PDF menu.
    elem = soup.find("strong", text=re.compile(week_pattern))
    pdf_url = "{}{}".format(ROOT_URL, elem.parent.parent.a["href"])

    response = requests.get(pdf_url, stream=True)
    # Save the menu to a file and run pdftotext on it.
    with tempfile.NamedTemporaryFile() as file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
        output = subprocess.check_output(["pdftotext", file.name, "-"]).lower().decode("utf-8")
    return output

def get_menu_output():
    output = extract_pdf_output()
    start_index, end_index = get_pdf_indexes()

    RE_STRING = r"({}.*?){}".format(start_index, end_index)

    regex_object = re.compile(RE_STRING, re.DOTALL)
    menu_output = re.search(regex_object, output).group(1)
    return menu_output

if __name__ == '__main__':
    print(get_menu_output())