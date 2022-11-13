import os
import sys
from typing import Callable, Dict

from scrapy import Spider, signals
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor
from scrapy.utils.log import configure_logging


def create_and_run_spider(spider_classes: list[Spider], results_callbacks: list[Callable], kwargs: list[Dict]):
    
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]

    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'Lib.WebScrapping.settings')
    settings = get_project_settings()

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(settings)
    crawl(runner, spider_classes, results_callbacks, kwargs)
    reactor.run()

@defer.inlineCallbacks
def crawl(runner: CrawlerRunner, spiders: list[Spider], callbacks: list[Callable], kwargs_callbacks: list[Callable]):
    runs = zip(spiders, callbacks, kwargs_callbacks)
    for run in runs:
        dispatcher.connect(run[1], signal=signals.item_scraped)
        yield runner.crawl(run[0], **run[2]())
        dispatcher.disconnect(run[1], signal=signals.item_scraped)
    reactor.stop()
