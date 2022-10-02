import sys
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--tags', '-t', nargs='+', help='Tags for keyword search', required=True)
argparser.add_argument('--pages', '-p', help='Number of Google pages to search through', type=int, required=True)
argparser.add_argument('--save-path', '-path', nargs='?', help='Folder path to save output to', type=str, default=".\Output", required=False)
argparser.add_argument('--n-gram-max', '-ngmax', nargs='?', help='Folder path to save output to', type=int, default=1, required=False)
args = argparser.parse_args()
tags = args.tags
pages = args.pages
ng_max = args.n_gram_max
pages = args.pages
save_path = args.save_path

from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *
from Lib.WebScrapping.SpiderInstance import *
from Lib.WebScrapping.CorpusScraper import *
from Lib.TextAnalytics.Methods import *
from Lib.Visualization.WordCloud import *

from os import path
from pathlib import Path
from datetime import datetime
import logging
from slugify import slugify
import json
from time import perf_counter

logging.disable(sys.maxsize)

gtc_start = perf_counter()
webpages = get_tag_corpus(tags, pages, methods=['Scholar'])
gtc_finish = perf_counter()

def build_folder_path(*args):
    csv_folder_path = Path(path.join(*args))
    csv_folder_path.mkdir(parents=True, exist_ok=True)
    return csv_folder_path

timestamp = datetime.now().strftime("%H-%M-%S")
all_text = ""

website_dict = dict()

for webpage in webpages:
    website_dict[webpage.url] = { "Website" : webpage.title, "Content" : webpage.textual_content, "FileType" : webpage.type }

search_results_dict = { "SearchParams" : { "Tags" : tags, "Pages" : pages, "SavePath" : save_path }, "Data" : website_dict, "Diagnostics" : { "SearchTimeTakenInSeconds" : f"{gtc_finish - gtc_start:0.3f}" } }
base_path = build_folder_path(save_path)

with open(f"{base_path}/{slugify(timestamp)}.json", "w") as out:
    json.dump(search_results_dict, out, indent=4)