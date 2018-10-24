#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

URL = "http://choicefood.dk/"

for i in range(3334):
    response = requests.get(URL, params={"ddownload": i})
    if response.status_code != 200:
        print(f"{response.request.url} is not a valid menu download link")
        continue
    print(f"{response.request.url} is valid!")
    filename = f"{i}.pdf"
    with open(filename, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf_file.write(chunk)
