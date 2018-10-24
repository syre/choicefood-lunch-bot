#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import glob
import nltk
import collections

nltk.download("punkt")

pdf_filenames = glob.glob("*.pdf")

menu_outputs = []

for filename in pdf_filenames:
    output = subprocess.check_output(
            ["pdftotext", filename, "-"]
        ).lower().decode("utf-8")
    menu_outputs.append(output)

tokens = []

for output in menu_outputs:
    tokens.extend(nltk.word_tokenize(output))
print(collections.Counter(tokens).most_common())