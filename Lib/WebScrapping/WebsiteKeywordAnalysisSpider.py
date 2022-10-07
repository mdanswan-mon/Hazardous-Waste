import scrapy
import textract
import os
import io
import tempfile
from PyPDF2 import PdfFileReader
from urllib.parse import urlparse
from urllib.parse import unquote
from Lib.Utilities import PdfProcessing

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

        file_types = self.get_file_type(response)
        selected_file_type = next((sup_file_type for (sup_file_type, sup_file_type_strs) in self.supported_file_types.items() if self.get_match_in_lists(sup_file_type_strs, file_types)), None)

        if selected_file_type:

            clean_file_type = selected_file_type.removeprefix(".").capitalize()
            resource_title, textual_content, resource_save_path = '', '', ''
            website_title = self.get_website_title(response)

            if clean_file_type in ['Html', 'Htm']:
                resource_title, textual_content = self.parse_document_as_html(response)
            elif clean_file_type in ['Pdf']:
                resource_title, textual_content = self.parse_document_as_pdf(response)
                resource_save_path = self.save_pdf(response.body, resource_title)
            else:
                resource_title, textual_content = self.parse_document_general(response, clean_file_type)

            if len(clean_file_type) > 0 and len(resource_title) > 0 and len(textual_content) > 0:
                yield { "content" : [response.url, clean_file_type, website_title, resource_title, textual_content, resource_save_path] }

    def save_pdf(self, bytes, title):
        if title.lower().endswith('.pdf'):
            resource_save_path = PdfProcessing.save_pdf(bytes, title.lower().removesuffix('.pdf'))
        else:
            resource_save_path = PdfProcessing.save_pdf(bytes, title)
        return resource_save_path

    def get_website_title(self, response):
        url_title = self.get_document_title_from_url(response.url)
        content_title = None
        try:
            content_title = response.css('title::text').extract_first().strip()
            title = content_title or url_title
        except:
            title = url_title
        return title

    def get_document_title_from_url(self, url):
        split_url = url.split('/')
        url_title = split_url[-1].strip()
        return unquote(url_title)
    
    def parse_document_general(self, response, file_type):
        title = self.get_document_title_from_url(response.url)
        temp_file, path = tempfile.mkstemp(suffix=file_type)
        try:
            with os.fdopen(temp_file, 'wb') as temp:
                temp.write(response.body)
        finally:
            textual_content = textract.process(path).decode('utf-8')
            os.remove(path)
        return [unquote(title), textual_content]
    
    def parse_document_as_html(self, response):
        title = self.get_website_title(response)
        elements = response.css('div::text, h1::text, h2::text, h3::text, h4::text, h5::text, h6::text, a::text, p::text, span::text, b::text, font::text').extract()
        textual_content = '\n~`~\n'.join([element.strip() for element in elements if len(element.strip()) > 0])
        return [unquote(title), textual_content]
    
    def parse_document_as_pdf(self, response):
        reader = PdfFileReader(io.BytesIO(response.body))
        title = reader.getDocumentInfo().title
        title = title.strip() if title else self.get_document_title_from_url(response.url)
        textual_content = ' '.join([page.extract_text() for page in reader.pages])
        return [unquote(title), textual_content]
        
    def get_file_type(self, response):
        content_type = response.headers['Content-Type'].decode('UTF-8')
        file_type_from_url = os.path.splitext(urlparse(response.url).path)[1]
        return [content_type, file_type_from_url]
    
    def get_match_in_lists(self, left, right):
        match = next((True for x in left for y in right if (x in y)), None)
        return match