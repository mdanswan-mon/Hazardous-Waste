import json
import os
import re

import pdf2doi
import slugify
from Lib.Utilities import PathHelpers

# Params: insensitive (i), single line (s)
CROSSREF_ABSTRACT_REGEX = '"abstract":"(.+?)(?=",".+")'
# Params: insensitive (i), single line (s)
CROSSREF_JATS_REGEX = '(<.*?>)'
# Params: insensitive (i)
WEBPAGE_ABSTRACT_REGEX = '(?i)(Abstract~`~)(.+?)(~`~)'

def get_doi_data_from_pdf(path):
    doi_data = ""
    try:
        pdf2doi.config.set('verbose', False)
        pdf2doi.config.set('websearch', False)
        doi_data = pdf2doi.pdf2doi(path)
    except:
        print(f"Unable to retrieve doi data for PDF at {path}")
    return doi_data

def get_abstract_from_cr_data(cross_ref_json: str):
    abstract = ""
    if cross_ref_json and len(cross_ref_json) > 0:
        try:
            search_result = re.search(CROSSREF_ABSTRACT_REGEX, cross_ref_json)
            if search_result:
                abstract_raw = search_result.group(1)
                abstract_clean = re.sub(CROSSREF_JATS_REGEX, '', abstract_raw)
                abstract_clean = abstract_clean.encode('utf-8').decode('unicode_escape')
                abstract_clean = abstract_clean.strip()
                abstract = abstract_clean
        except Exception as e:
            print(f"{str(e)}\nUnable to parse cross ref data to retrieve abstract: {cross_ref_json}")
    return abstract

# TODO: abstract out preprocessing of cross_ref_json data (mainly new_str = unicodedata.normalize("NFKD", unicode_str) - https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python)

def get_abstract_from_text(text: str):
    abstract = ""
    if text and len(text) > 0:
        try:
            search_result = re.search(WEBPAGE_ABSTRACT_REGEX, text)
            if search_result:
                abstract_raw = search_result.group(2)
                abstract_clean = re.sub('\\n~`~\\n', ' ', abstract_raw)
                abstract_clean = abstract_clean.encode('utf-8').decode('unicode_escape')
                abstract_clean = abstract_clean.strip()
                abstract = abstract_clean
        except:
            print(f"Unable to parse text to retrieve abstract: {text}")
    return abstract

def save_pdf(pdf: bytes, filename: str, path="./Output/Files"):
    folder_path = PathHelpers.build_folder_path(path)
    full_path = os.path.join(folder_path.resolve().absolute(), slugify.slugify(filename)) + '.pdf'
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
        with open(full_path, "wb") as file:
            file.write(pdf)
    except:
        return ""
    return full_path
