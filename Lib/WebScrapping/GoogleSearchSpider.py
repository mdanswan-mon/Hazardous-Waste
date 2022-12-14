import scrapy
import urllib

class GoogleSearch(scrapy.Spider):
    
    name = 'GoogleSearch'
    
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs['base_url']
        self.tags = kwargs['tags']
        self.pages = kwargs['pages']
        self.websites_to_ignore = [website.strip() for website in open('Resources/websites-to-ignore.txt', 'r').readlines() if not website.startswith("#")]
        super().__init__(self.name, **kwargs)
    
    def start_requests(self):
        for x in range(self.pages):
            url = self.base_url.format(f"{urllib.parse.quote(' '.join(self.tags))}", 10 * x)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):        
        print(f"Running Google Search at {response.url}")
        search_items = response.css('.fP1Qef').extract()
        searches = []
        for search in search_items:
            selector = scrapy.Selector(text=search)
            link = selector.css('a::attr(href)').get()
            if not any(website in link for website in self.websites_to_ignore):
                link = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)['q'][0]
                searches.append(link)
        yield { "urls": searches }