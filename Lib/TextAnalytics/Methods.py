from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def get_countvectorizer(text, stopwords = [], ng_min = 1, ng_max = 1):
    count_vec = CountVectorizer(stop_words=stopwords, ngram_range=(ng_min, ng_max))
    X = count_vec.fit_transform([text])
    return [X, count_vec]

def get_tfidf(corpus, stopwords = [], ng_min = 1, ng_max = 1):
    freq_vec = TfidfVectorizer(stop_words=stopwords, ngram_range=(ng_min, ng_max))
    X = freq_vec.fit_transform(corpus)
    return [X, freq_vec]