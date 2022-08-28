import sys
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--tags', '-t', nargs='+', help='Tags for keyword search', required=True)
argparser.add_argument('--pages', '-p', help='Number of Google pages to search through', type=int, required=True)
argparser.add_argument('--save-occurrences', '-occ', help='Save the occurrence counts of each word for each website', action=argparse.BooleanOptionalAction)
argparser.add_argument('--save-wordclouds', '-clouds', help='Save the word cloud visualization of each website', action=argparse.BooleanOptionalAction)
argparser.add_argument('--save-path', '-path', nargs='?', help='Folder path to save output to', type=str, default=".\Output", required=False)
argparser.add_argument('--n-gram-min', '-ngmin', nargs='?', help='The minimum amount of matching words', type=int, default=1, required=False)
argparser.add_argument('--n-gram-max', '-ngmax', nargs='?', help='Folder path to save output to', type=int, default=1, required=False)
args = argparser.parse_args()
tags = args.tags
pages = args.pages
ng_min = args.n_gram_min
ng_max = args.n_gram_max
pages = args.pages
save_occs = args.save_occurrences
save_wordclouds = args.save_wordclouds
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
import numpy as np
import pandas as pd 
from slugify import slugify
from PIL import Image

logging.disable(sys.maxsize)

webpages = get_tag_corpus(tags, pages)

def get_keyword_occurrences_as_dict(occurrences, vectorizer):
    keywords = vectorizer.get_feature_names_out()
    occurrences = occurrences.toarray()[0]
    return dict(zip(keywords, occurrences))

def save_occurrences(path):
    print(f"Saving occurrences to {path}")
    pd.DataFrame.from_dict(keyword_analysis_dict, 'index').to_csv(path)

def build_folder_path(*args):
    csv_folder_path = Path(path.join(*args))
    csv_folder_path.mkdir(parents=True, exist_ok=True)
    return csv_folder_path

stop_words = [word.strip() for word in open('Resources/stop-words.txt', 'r').readlines()]
circle_mask = np.array(Image.open('Resources/circle.png'))
timestamp = datetime.now().strftime("%H-%M-%S")
all_text = ""

for index, webpage in enumerate(webpages):
    keyword_text = webpage.textual_content
    keyword_analysis = get_occurrences(keyword_text, stop_words, ng_min, ng_max)
    keyword_analysis_dict = get_keyword_occurrences_as_dict(keyword_analysis[0], keyword_analysis[1])
    website_name = slugify(webpage.title, max_length=50) if webpage.title is not None else 'Unknown'
    base_path = build_folder_path(save_path, f"{slugify('-'.join(tags), max_length=80)}-{timestamp}", str(index + 1))
    if (save_occs):
        save_occurrences(path.join(base_path, "occurrences.csv"))
    if (save_wordclouds):
        save_word_cloud(keyword_analysis_dict, circle_mask, path.join(base_path, "wordcloud.png"))
    with open(path.join(base_path, "website-info.txt"), 'a+') as md:
        md.write(f'Website Name: {website_name}\n')
        md.write(f'Website URL: {webpage.url}\n')
        md.write(f'Total Words: {len(keyword_analysis_dict)}')
    all_text = all_text + keyword_text
    
keyword_analysis = get_occurrences(all_text, stop_words, ng_min, ng_max)
keyword_analysis_dict = get_keyword_occurrences_as_dict(keyword_analysis[0], keyword_analysis[1])
base_path = build_folder_path(save_path, f"{slugify('-'.join(tags), max_length=80)}-{timestamp}", "aggregate")
if (save_occs):
    save_occurrences(path.join(base_path, "occurrences.csv"))
if (save_wordclouds):
    save_word_cloud(keyword_analysis_dict, circle_mask, path.join(base_path, "wordcloud.png"))