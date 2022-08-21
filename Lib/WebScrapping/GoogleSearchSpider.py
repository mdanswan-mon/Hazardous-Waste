import scrapy
import urllib

class GoogleSearch(scrapy.Spider):
    
    name = 'GoogleSearch'
    
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs['base_url']
        self.tags = kwargs['tags']
        self.pages = kwargs['pages']
        super().__init__(self.name, **kwargs)
    
    def start_requests(self):
        for x in range(self.pages):
            url = self.base_url.format(f"{urllib.parse.quote(' '.join(self.tags))}", 10 * x)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):        
        print(f"Running Google Search at {response.url}")
        search_items = response.css('.fP1Qef').extract()
        searches = dict()
        for search in search_items:
            selector = scrapy.Selector(text=search)
            title = selector.xpath('//a/h3/div//text()').get()
            link = selector.css('a::attr(href)').get()
            link = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)['q'][0]
            if title not in searches.keys():
                searches[title] = link
        yield searches