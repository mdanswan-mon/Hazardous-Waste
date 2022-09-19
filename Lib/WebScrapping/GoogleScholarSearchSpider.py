import scrapy
import urllib

class GoogleScholarSearch(scrapy.Spider):
    
    name = 'GoogleScholarSearch'
    
    def __init__(self, *args, **kwargs):
        self.base_url = "https://scholar.google.com.au/scholar?as_q={0}&as_publication={1}&as_ylo={2}&as_yhi={3}&start={4}"
        self.tags = kwargs['tags']
        self.pages = kwargs['pages']
        self.publications = kwargs['pubs']
        self.from_year = kwargs['from_year']
        self.to_year = kwargs['to_year']
        super().__init__(self.name, **kwargs)
    
    def start_requests(self):
        for x in range(self.pages):
            url = self.base_url.format(f"{urllib.parse.quote(' '.join(self.tags))}", f"{urllib.parse.quote(' '.join(self.publications))}", self.from_year, self.to_year, 10 * x)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):        
        print(f"Running Google Search at {response.url}")
        search_items = response.xpath('//div[@class="gs_r gs_or gs_scl"]').extract()
        searches = []
        for search in search_items:
            selector = scrapy.Selector(text=search)
            link = selector.css('.gs_or_ggsm > a::attr(href)').get()
            if link:
                searches.append(link)
        yield { "urls": searches }