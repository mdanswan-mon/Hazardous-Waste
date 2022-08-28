from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def get_occurrences(text, stopwords, ng_min, ng_max):
    count_vec = CountVectorizer(stop_words=stopwords, ngram_range=(ng_min, ng_max))
    X = count_vec.fit_transform([text])
    return [X, count_vec]

def get_frequency(corpus, stopwords, ng_min, ng_max):
    freq_vec = TfidfVectorizer(stop_words=stopwords, ngram_range=(ng_min, ng_max))
    X = freq_vec.fit_transform(corpus)
    return [X, freq_vec]