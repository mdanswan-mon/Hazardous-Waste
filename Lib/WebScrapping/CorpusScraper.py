from time import perf_counter
from Lib.TextAnalytics.Methods import *
from Lib.Utilities import PdfProcessing
from Lib.Visualization.WordCloud import *
from Lib.WebScrapping.GoogleScholarSearchSpider import *
from Lib.WebScrapping.GoogleSearchSpider import *
from Lib.WebScrapping.SpiderInstance import *
from Lib.WebScrapping.Webpage import Webpage
from Lib.WebScrapping.WebsiteKeywordAnalysisSpider import *

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
                webpage.resource_type = webpage_content[1]
                webpage.website_title = webpage_content[2]
                webpage.resource_title = webpage_content[3]
                webpage.textual_content = webpage_content[4]
                webpage.resource_save_path = webpage_content[5]
                if webpage.resource_save_path:
                    doi_data = PdfProcessing.get_doi_data_from_pdf(webpage.resource_save_path)
                    if doi_data:
                        if 'identifier' in doi_data:
                            webpage.doi = doi_data['identifier']
                        if 'validation_info' in doi_data:
                            webpage.cross_ref_data = doi_data['validation_info']
                            abstract = PdfProcessing.get_abstract_from_cr_data(webpage.cross_ref_data)
                            if len(abstract) == 0:
                                abstract = PdfProcessing.get_abstract_from_text(webpage.textual_content)
                            webpage.abstract = abstract
                break

    create_and_run_spider([GoogleScholarSearch, WebsiteKeywordAnalysis], \
                            [google_search_results_listener, keyword_analysis_results_listener], \
                            [lambda: { "tags": tags, "pages": pages, "pubs": [], "from_year": from_year, "to_year": to_year }, \
                            lambda: { "urls": [webpage.url for webpage in webpages] }])

    # valid_webpages: list[Webpage] = list()

    # for webpage in webpages:
    #     if len(webpage.website_title) > 0 and len(webpage.resource_title) > 0 and len(webpage.textual_content) > 0:
    #         valid_webpages.append(webpage)
            
    return webpages
