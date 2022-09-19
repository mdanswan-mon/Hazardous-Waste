from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.GoogleScholarSearchSpider import *
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *
from Lib.WebScrapping.SpiderInstance import *
from Lib.WebScrapping.Webpage import Webpage
from Lib.TextAnalytics.Methods import *
from Lib.Visualization.WordCloud import *

def get_tag_corpus(tags, pages=1, methods=['Search', 'Scholar'], publications=[], from_year='', to_year=''):

    webpages: list[Webpage] = list()

    def google_search_results_listener(signal, sender, item, response, spider):
        nonlocal webpages
        urls = item['urls'] if 'urls' in item.keys() else None
        if urls is not None:
            for url in urls:
                webpages.append(Webpage(url=url))

    def keyword_analysis_results_listener(signal, sender, item, response, spider):
        nonlocal webpages
        webpage_content = item['content']
        for webpage in webpages:
            if (webpage.url == webpage_content[0]):
                webpage.type = webpage_content[1]
                webpage.title = webpage_content[2]
                webpage.textual_content = webpage_content[3]
                break

    if 'Search' in methods:
        create_and_run_spider(GoogleSearch, google_search_results_listener, base_url="https://www.google.com.au/search?q={0}&start={1}", tags=tags, pages=pages)

    if 'Scholar' in methods:
        create_and_run_spider(GoogleScholarSearch, google_search_results_listener, tags=tags, pages=pages, pubs=[], from_year=from_year, to_year=to_year)

    for webpage in webpages:
        create_and_run_spider(WebsiteKeywordAnalysis, keyword_analysis_results_listener, base_url=webpage.url)

    valid_webpages: list[Webpage] = list()

    for webpage in webpages:
        if len(webpage.title) > 0 and len(webpage.textual_content) > 0 and len(webpage.textual_content) > 0:
            valid_webpages.append(webpage)

    return valid_webpages