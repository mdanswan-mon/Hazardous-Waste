import sys
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--tags', '-t', nargs='+', help='Tags for keyword search', required=True)
argparser.add_argument('--pages', '-p', help='Number of Google pages to search through', type=int, required=True)
argparser.add_argument('--save-occurrences', '-occ', help='Save the occurrence counts of each word for each website', action=argparse.BooleanOptionalAction)
argparser.add_argument('--save-wordclouds', '-clouds', help='Save the word cloud visualization of each website', action=argparse.BooleanOptionalAction)
argparser.add_argument('--save-path', '-path', nargs='?', help='Folder path to save output to', type=str, default=".\Output", required=False)
args = argparser.parse_args()
tags = args.tags
pages = args.pages
save_occs = args.save_occurrences
save_wordclouds = args.save_wordclouds
save_path = args.save_path

from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *
from Lib.WebScrapping.SpiderInstance import *

from os import path
from collections import ChainMap
from pathlib import Path
from datetime import datetime
import logging
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from slugify import slugify
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from PIL import Image

logging.disable(sys.maxsize)

keyword_analysis_results = dict()
google_search_results = []

def google_search_results_listener(signal, sender, item, response, spider):
    global google_search_results
    google_search_results.append(item)
    
def keyword_analysis_results_listener(signal, sender, item, response, spider):
    global keyword_analysis_results
    keyword_analysis_results[list(item.keys())[0]] = list(item.values())[0]

result = create_and_run_spider(GoogleSearch, google_search_results_listener, base_url="https://www.google.com.au/search?q={0}&start={1}", tags=tags, pages=pages)

for page in google_search_results:
    for website_name, url in page.items():
        result = create_and_run_spider(WebsiteKeywordAnalysis, keyword_analysis_results_listener, base_url=url, website=website_name)
        
stop_words = [word.strip() for word in open('Resources/stop-words.txt', 'r').readlines()]

def count_occurrences(text):
    count_vec = CountVectorizer(stop_words=stop_words)
    X = count_vec.fit_transform([text])
    return [X, count_vec]

def get_keyword_occurrences_as_dict(occurrences, vectorizer):
    keywords = vectorizer.get_feature_names_out()
    occurrences = occurrences.toarray()[0]
    return dict(zip(keywords, occurrences))

circle_mask = np.array(Image.open('Resources/circle.png'))

def draw_word_cloud(keyword_analysis_dict):
    wordcloud = WordCloud(width=1000, height=666, random_state=1, background_color='white', colormap='inferno', collocations=False, mask=circle_mask).generate_from_frequencies(keyword_analysis_dict)
    plt.figure(figsize=(10, 15))
    plt.imshow(wordcloud)
    plt.axis("off")
    
def save_word_cloud(keyword_analysis_dict, path, dpi=300):
    wordcloud = WordCloud(width=1000, height=666, random_state=1, background_color='white', colormap='inferno', collocations=False, mask=circle_mask).generate_from_frequencies(keyword_analysis_dict)
    print(f"Saving word cloud to {path}")
    plt.figure(figsize=(10, 15))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(path, dpi=dpi)
    plt.close(plt.gcf())
    
def save_occurrences(path):
    print(f"Saving occurrences to {path}")
    pd.DataFrame.from_dict(keyword_analysis_dict, 'index').to_csv(path)

def build_folder_path(*args):
    csv_folder_path = Path(path.join(*args))
    csv_folder_path.mkdir(parents=True, exist_ok=True)
    return csv_folder_path

all_text = ""
timestamp = datetime.now().strftime("%H-%M-%S")
all_websites = ChainMap(*google_search_results)

for index, website in enumerate(keyword_analysis_results):
    keyword_text = keyword_analysis_results[website]
    keyword_analysis = count_occurrences(keyword_text)
    keyword_analysis_dict = get_keyword_occurrences_as_dict(keyword_analysis[0], keyword_analysis[1])
    website_name = slugify(website, max_length=50) if website is not None else 'Unknown'
    website_url = all_websites[website]
    base_path = build_folder_path(save_path, f"{slugify('-'.join(tags), max_length=80)}-{timestamp}", str(index + 1))
    if (save_occs):
        save_occurrences(path.join(base_path, "occurrences.csv"))
    if (save_wordclouds):
        save_word_cloud(keyword_analysis_dict, path.join(base_path, "wordcloud.png"))
    with open(path.join(base_path, "website-info.txt"), 'a+') as md:
        md.write(f'Website Name: {website_name}\n')
        md.write(f'Website URL: {website_url}\n')
        md.write(f'Total Words: {len(keyword_analysis_dict)}')
    all_text = all_text + keyword_text
    
keyword_analysis = count_occurrences(all_text)
keyword_analysis_dict = get_keyword_occurrences_as_dict(keyword_analysis[0], keyword_analysis[1])
base_path = build_folder_path(save_path, f"{slugify('-'.join(tags), max_length=80)}-{timestamp}", "aggregate")
if (save_occs):
    save_occurrences(path.join(base_path, "occurrences.csv"))
if (save_wordclouds):
    save_word_cloud(keyword_analysis_dict, path.join(base_path, "wordcloud.png"))