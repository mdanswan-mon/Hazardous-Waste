import scrapy

class WebsiteKeywordAnalysis(scrapy.Spider):
    
    name = 'WebsiteKeywordAnalysis'
    
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs['base_url']
        self.website = kwargs['website']
        super().__init__(self.name, **kwargs)
    
    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)
        
    def parse(self, response):
        print(f"Running keyword collection at {response.url}")
        elements = response.css('div::text, h1::text, h2::text, h3::text, h4::text, h5::text, h6::text, a::text, p::text').extract()
        combined_string = ' '.join(elements)
        yield { self.website: combined_string }