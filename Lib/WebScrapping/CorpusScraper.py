from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *
from Lib.WebScrapping.SpiderInstance import *
from Lib.WebScrapping.Webpage import Webpage
from Lib.TextAnalytics.Methods import *
from Lib.Visualization.WordCloud import *

def get_tag_corpus(tags, pages):

    webpages: list[Webpage] = list()

    def google_search_results_listener(signal, sender, item, response, spider):
        nonlocal webpages
        urls = item['urls']
        for url in urls:
            webpages.append(Webpage(url=url))
        
    def keyword_analysis_results_listener(signal, sender, item, response, spider):
        nonlocal webpages
        webpage_content = item['content']
        for webpage in webpages:
            if (webpage.url == webpage_content[0]):
                webpage.title = webpage_content[1]
                webpage.textual_content = webpage_content[2]

    create_and_run_spider(GoogleSearch, google_search_results_listener, base_url="https://www.google.com.au/search?q={0}&start={1}", tags=tags, pages=pages)

    for webpage in webpages:
        create_and_run_spider(WebsiteKeywordAnalysis, keyword_analysis_results_listener, base_url=webpage.url)
        
    return webpages