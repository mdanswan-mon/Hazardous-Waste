import sys
import argparse

# argparser = argparse.ArgumentParser()
# argparser.add_argument('--tags', '-t', nargs='+', help='Tags for keyword search', required=True)
# argparser.add_argument('--pages', '-p', help='Number of Google pages to search through', type=int, required=True)
# argparser.add_argument('--save-path', '-path', nargs='?', help='Folder path to save output to', type=str, default=".\Output", required=False)
# argparser.add_argument('--n-gram-max', '-ngmax', nargs='?', help='Folder path to save output to', type=int, default=1, required=False)
# args = argparser.parse_args()
# tags = args.tags
# pages = args.pages
# ng_max = args.n_gram_max
# save_path = args.save_path
tags = ['microplastic', 'waste', 'marine']
pages = 10
ng_max = 1
save_path = "./Output"

from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *
from Lib.WebScrapping.SpiderInstance import *
from Lib.WebScrapping.CorpusScraper import *
from Lib.TextAnalytics.Methods import *
from Lib.Utilities import PathHelpers
from Lib.Utilities import PdfProcessing

from datetime import datetime
import logging
from slugify import slugify
import json
from time import perf_counter

logging.disable(sys.maxsize)

gtc_start = perf_counter()
webpages = get_tag_corpus(tags, pages, methods=['Scholar'], from_year=2015)
gtc_finish = perf_counter()

timestamp = datetime.now().strftime("%d/%m/%y_%H-%M-%S")
all_text = ""

website_dict = dict()

for webpage in webpages:
    if webpage.resource_save_path and webpage.resource_type == "Pdf":
        doi_data = PdfProcessing.get_doi_data_from_pdf(webpage.resource_save_path)
        if doi_data:
            if 'identifier' in doi_data:
                webpage.doi = doi_data['identifier']
            if 'validation_info' in doi_data:
                webpage.cross_ref_data = doi_data['validation_info']
                webpage.abstract = PdfProcessing.get_abstract_from_cr_data(webpage.cross_ref_data)

for webpage in webpages:
    website_dict[webpage.url] = { "WebsiteTitle" : webpage.website_title, "ResourceTitle" : webpage.resource_title, "ResourceType" : webpage.resource_type, "ResourceSavePath" : webpage.resource_save_path, "DOI" : webpage.doi, "Abstract" : webpage.abstract, "RawText" : webpage.textual_content }

search_results_dict = { "SearchParams" : { "Tags" : tags, "Pages" : pages, "SavePath" : save_path }, "Data" : website_dict, "Diagnostics" : { "SearchTimeTakenInSeconds" : f"{gtc_finish - gtc_start:0.3f}" } }
base_path = PathHelpers.build_folder_path(save_path)

with open(f"{base_path}/{slugify(timestamp)}.json", "w") as out:
    json.dump(search_results_dict, out, indent=4)