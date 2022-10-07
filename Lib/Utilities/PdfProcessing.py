import pdf2doi
import os
import slugify
import json
import re

from Lib.Utilities import PathHelpers

def get_doi_data_from_pdf(path):
    doi_data = ""
    try:
        pdf2doi.config.set('verbose', False)
        pdf2doi.config.set('websearch', True)
        doi_data = pdf2doi.pdf2doi(path)
    except:
        print(f"Unable to retrieve doi data for PDF at {path}")
    return doi_data

def get_abstract_from_cr_data(cross_ref_data : str):
    abstract = ""
    if cross_ref_data and len(cross_ref_data) > 0:
        try:
            data = json.loads(cross_ref_data)
            if 'abstract' in data:
                abstract = re.search('(<jats:p>|<p>)(.+?)(</jats:p>|</p>)', data['abstract']).group(2)
        except:
            print(f"Unable to parse cross ref data to retrieve abstract: {cross_ref_data}")
    return abstract

def get_abstract_from_text(text : str):
    abstract = ""
    if text and len(text) > 0:
        try:
            abstract = re.search('(<jats:p>|<p>)(.+?)(</jats:p>|</p>)', text).group(2)
        except:
            print(f"Unable to parse text to retrieve abstract: {text}")
    return abstract

def save_pdf(pdf : bytes, filename : str, path="./Output/Files"):
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