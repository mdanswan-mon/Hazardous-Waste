import scrapy
import textract
import os
import tempfile
from PyPDF2 import PdfReader
from urllib.parse import urlparse

class WebsiteKeywordAnalysis(scrapy.Spider):
    
    name = 'WebsiteKeywordAnalysis'
    
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs['base_url']
        self.supported_file_types = { file_type.strip().split('=')[0]:file_type.strip().split('=')[1].split(',') for file_type in open('Resources/supported-file-types.txt', 'r').readlines() if not file_type.startswith("#") }
        super().__init__(self.name, **kwargs)
    
    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)
        
    def parse(self, response):
        print(f"Running keyword collection at {response.url}")
        title, combined_string = '', ''
        
        file_types = self.get_file_type(response)
        selected_file_type = next((sup_file_type for (sup_file_type, sup_file_type_strs) in self.supported_file_types.items() if self.get_match_in_lists(sup_file_type_strs, file_types)), None)
        
        if selected_file_type:
            clean_file_type = selected_file_type.removeprefix(".").capitalize()
            
            temp_file, path = tempfile.mkstemp(suffix=selected_file_type)
            try:
                with os.fdopen(temp_file, 'wb') as temp:
                    temp.write(response.body)
            finally:
                combined_string = textract.process(path).decode('utf-8')
                
            title = self.get_title(response, clean_file_type, path)
            
            os.remove(path)
            
            if len(clean_file_type) > 0 and len(title) > 0 and len(combined_string) > 0:
                yield { "content" : [response.url, clean_file_type, title, combined_string] }
        
    def get_title(self, response, file_type, file_path):
        split_url = response.url.split('/')
        url_title = split_url[-1].strip()
        if "html" in file_type.lower():
            return response.css('title::text').extract_first().strip() or url_title
        elif "pdf" in file_type.lower():
            reader = PdfReader(file_path)
            return reader.getDocumentInfo().title.strip() or url_title
        else:
            return url_title
        
    def get_file_type(self, response):
        content_type = response.headers['Content-Type'].decode('UTF-8')
        file_type_from_url = os.path.splitext(urlparse(response.url).path)[1]
        return [content_type, file_type_from_url]
    
    def get_match_in_lists(self, left, right):
        match = next((True for x in left for y in right if (x in y)), None)
        return match