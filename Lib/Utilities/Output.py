import csv
import json
from datetime import datetime
from typing import List

from Lib.Utilities import PathHelpers
from Lib.WebScrapping.Webpage import Webpage
from slugify import slugify


def get_date_time_filename():
    timestamp = datetime.now().strftime("%d/%m/%y_%H-%M-%S")
    return timestamp

def write_webpages_to_csv(webpages : List[Webpage], save_path: str="Output"):
    base_path = PathHelpers.build_folder_path(save_path)
    timestamp = get_date_time_filename()
    abs_path = f"{base_path}/{slugify(timestamp)}.csv"
    with open(abs_path, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for webpage in webpages:
            writer.writerow([webpage.url])
    return abs_path
            
def write_search_results_to_json(webpages : List[Webpage], tags: List, pages: int, search_time: str, save_path: str="Output"):
    base_path = PathHelpers.build_folder_path(save_path)
    timestamp = get_date_time_filename()
    abs_path = f"{base_path}/{slugify(timestamp)}.json"
    with open(abs_path, 'w+') as json_file:
        website_dict = dict()
        for webpage in webpages:
            website_dict[webpage.url] = { "WebsiteTitle" : webpage.website_title, "ResourceTitle" : webpage.resource_title, "ResourceType" : webpage.resource_type, "ResourceSavePath" : webpage.resource_save_path, "DOI" : webpage.doi, "Abstract" : webpage.abstract, "CrossRefData": webpage.cross_ref_data, "Text" : webpage.textual_content }
        search_results_dict = { "SearchParams" : { "Tags" : tags, "Pages" : pages, "SavePath" : save_path }, "Data" : website_dict, "Diagnostics" : { "SearchTimeTakenInSeconds" : search_time } }
        json.dump(search_results_dict, json_file, indent=4)
    return abs_path

def write_classification_results_to_csv(doc_urls : List[str], classes: List[str], save_path: str="Output/RelevanceClassification"):
    base_path = PathHelpers.build_folder_path(save_path)
    timestamp = get_date_time_filename()
    abs_path = f"{base_path}/{slugify(timestamp)}.json"
    with open(abs_path, 'w+') as json_file:
        results_dict = dict()
        for (doc_url, doc_class) in zip(doc_urls, classes):
            results_dict[doc_url] = { "Class" : doc_class }
        json.dump(results_dict, json_file, indent=4)
    return abs_path
