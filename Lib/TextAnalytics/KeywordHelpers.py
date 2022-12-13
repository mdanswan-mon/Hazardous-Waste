import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

def stem_keywords(list : np.ndarray):
    stemmer = SnowballStemmer("english")
    return np.unique(np.array([stemmer.stem(word) for word in list]))

def lemmatize_keywords(list : np.ndarray):
    lemmatizer = WordNetLemmatizer()
    return np.unique(np.array([lemmatizer.lemmatize(word) for word in list]))

def get_vocabulary(lists : np.ndarray):
    vocabulary = np.unique(np.hstack(lists))
    return vocabulary

def get_keyword_mask(vocabulary : np.ndarray, keywords : np.ndarray):
    for kw in keywords:
        if kw not in vocabulary:
            print(kw, "not in", vocabulary)
    return np.in1d(vocabulary, keywords)