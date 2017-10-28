import re

import os


def load_stopwords(stopwords_file='stopwords.txt'):
    stop_words = []
    r_unwanted = re.compile("[\n\t\r]")

    if os.path.isfile(stopwords_file) and os.access(stopwords_file, os.R_OK):
        with open(stopwords_file) as f:
            lines = f.readlines()
            lines = [line.lower() for line in lines]
            lines = [r_unwanted.sub('', line) for line in lines]
            stop_words += lines

