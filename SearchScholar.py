import argparse
import sys

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
tags = ['microplastic', 'waste', 'hazard', 'marine']
pages = 5
ng_max = 1
save_path = "./Output"

import logging
from time import perf_counter

from Lib.TextAnalytics.Methods import *
from Lib.Utilities import Output
from Lib.WebScrapping.CorpusScraper import *
from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.SpiderInstance import *
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *

logging.disable(sys.maxsize)

gtc_start = perf_counter()
webpages = get_tag_corpus(tags, pages, methods=['Scholar'], from_year=2015)
gtc_finish = perf_counter()

website_dict = dict()

search_time = f"{gtc_finish - gtc_start:0.3f}"

Output.write_webpages_to_csv(webpages)
Output.write_search_results_to_json(webpages, tags, pages, search_time)
