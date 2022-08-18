import sys
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

def create_and_run_spider(spider_class, results_callback, **kwargs):
    
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]
            
    dispatcher.connect(results_callback, signal=signals.item_scraped)
    process = CrawlerProcess()
    process.crawl(spider_class, **kwargs)
    process.start()