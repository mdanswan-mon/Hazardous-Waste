import spacy
import yake
import pytextrank
from rake_nltk import Rake
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def get_countvectorizer(text, stopwords = [], ng_min = 1, ng_max = 1):
    count_vec = CountVectorizer(stop_words=stopwords, ngram_range=(ng_min, ng_max))
    X = count_vec.fit_transform([text])
    return [X, count_vec]

def get_tfidf(corpus, stopwords = [], ng_min = 1, ng_max = 1):
    swords = stopwords if len(stopwords) > 0 else None
    freq_vec = TfidfVectorizer(stop_words=swords, ngram_range=(ng_min, ng_max), strip_accents='unicode', decode_error='replace', min_df=5)
    X = freq_vec.fit_transform(corpus)
    return [X, freq_vec]

def get_keywords_spacy(text):
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("textrank")
    result = nlp(text.lower())
    return result

# Rake - Frequency Analysis with consideration of co-occurrence
def get_keywords_rake_nltk(text, ngram_max = 3, stopwords = None):
    rake = Rake(max_length=ngram_max, stopwords=stopwords, include_repeated_phrases=False)
    rake.extract_keywords_from_text(text)
    result = rake.get_ranked_phrases_with_scores()
    return result

def get_keywords_yake(text, ngram_max = 1, num_results = 10, stopwords = None):
    extractor = yake.KeywordExtractor(n=ngram_max, top=num_results, stopwords=stopwords)
    result = extractor.extract_keywords(text)
    return result

def get_keywords_keybert(text, ngram_max = 1, num_results = 10, stopwords = None):
    keyBert = KeyBERT()
    result = keyBert.extract_keywords(text, stop_words=stopwords, top_n=num_results)
    return result