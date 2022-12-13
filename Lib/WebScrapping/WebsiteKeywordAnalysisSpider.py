import io
import os
import re
import tempfile
from urllib.parse import unquote, urlparse
from scrapy.utils.python import to_native_str
from six.moves.urllib.parse import urljoin

import scrapy
import textract
from fpdf import FPDF
from Lib.Utilities import PdfProcessing
from PyPDF2 import PdfFileReader

class WebsiteKeywordAnalysis(scrapy.Spider):
    
    name = 'WebsiteKeywordAnalysis'
    
    def __init__(self, *args, **kwargs):
        self.urls = kwargs['urls']
        self.supported_file_types = { file_type.strip().split('=')[0]:file_type.strip().split('=')[1].split(',') for file_type in open('Resources/supported-file-types.txt', 'r').readlines() if not file_type.startswith("#") }
        super().__init__(self.name, **kwargs)
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
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
                pdf_bytes = self.text_to_pdf_bytes(textual_content)
                resource_save_path = self.save_pdf(pdf_bytes, resource_title)
            elif clean_file_type in ['Pdf']:
                resource_title, textual_content = self.parse_document_as_pdf(response)
                resource_save_path = self.save_pdf(response.body, resource_title)
            else:
                resource_title, textual_content = self.parse_document_general(response, clean_file_type)

            if len(clean_file_type) > 0 and len(resource_title) > 0 and len(textual_content) > 0:
                url = response.request.meta['redirect_urls'][0] if 'redirect_urls' in response.request.meta else response.url
                yield { "content" : [url, clean_file_type, website_title, resource_title, textual_content, resource_save_path] }

    def text_to_pdf_bytes(self, text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_xy(0, 0)
        pdf.set_font('arial', 'B', 12.0)
        latin_encoded_text = text.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(h = 5.0, align='J', w = 0, txt=latin_encoded_text, border=0)
        bytes = pdf.output(dest='S').encode('latin-1')
        return bytes

    def save_pdf(self, bytes, title):
        title = re.sub('.pdf', '', title, flags=re.IGNORECASE)
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
        split_url = url.split('/')[-1].strip()
        split_url_wo_query = split_url.split('?')[0].strip()
        url_title = split_url_wo_query
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
        return [unquote(title), textual_content.strip()]
    
    def parse_document_as_html(self, response):
        title = self.get_website_title(response)
        elements = response.css('div::text, h1::text, h2::text, h3::text, h4::text, h5::text, h6::text, a::text, p::text, span::text, b::text, font::text').extract()
        textual_content = '~`~'.join([element.strip() for element in elements if len(element.strip())])
        return [unquote(title), textual_content.strip()]
    
    def parse_document_as_pdf(self, response):
        reader = PdfFileReader(io.BytesIO(response.body))
        if reader.is_encrypted:
            try:
                if reader.decrypt('') == 0:
                    return ["", ""]
            except:
                return ["", ""]
        title = reader.getDocumentInfo().title
        title = title.strip() if title else self.get_document_title_from_url(response.url)
        textual_content = ' '.join([page.extract_text() for page in reader.pages])
        return [unquote(title), textual_content.strip()]
        
    def get_file_type(self, response):
        content_type = response.headers['Content-Type'].decode('UTF-8')
        file_type_from_url = os.path.splitext(urlparse(response.url).path)[1]
        return [content_type, file_type_from_url]
    
    def get_match_in_lists(self, left, right):
        match = next((True for x in left for y in right if (x in y)), None)
        return match
