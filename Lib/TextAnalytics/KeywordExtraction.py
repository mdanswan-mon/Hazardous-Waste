import json

import numpy as np
from Lib.PreProcessing.General import *
from Lib.TextAnalytics.Methods import *
from Lib.TextAnalytics.KeywordHelpers import *
from Lib.WebScrapping.CorpusScraper import *

def extract_keywords_from_results(json_filepath):
    with open(json_filepath, 'r+') as file:
        data = json.load(file)
        corpus = { webpage : remove_stop_words(data['Data'][webpage]['Abstract'], 'Resources/stop-words.txt') for webpage in data['Data'] if len(data['Data'][webpage]['Abstract'].strip()) > 0 }
        keywords = np.empty(shape=(len(corpus), 2), dtype=object)

        for idx, (key, processed_text) in enumerate(corpus.items()):
            keybert_kw = lemmatize_keywords(np.array([keyword[0] for keyword in get_keywords_keybert(processed_text)]))
            keywords[idx, 0] = key
            keywords[idx, 1] = keybert_kw
        
        vocabulary = get_vocabulary(keywords[:, 1])
        
        keybert_results = np.empty(shape=(len(keywords[:, 1]), len(vocabulary)))

        for idx, row in enumerate(keywords[:, 1]):
            keybert_results[idx] = get_keyword_mask(vocabulary, row)
        
        return (keybert_results, vocabulary)
