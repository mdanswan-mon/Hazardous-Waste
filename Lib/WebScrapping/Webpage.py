class Webpage:
    
    def __init__(self, resource_type = "", website_title = "", url = "", textual_content = "", resource_title = "", resource_save_path = "", doi = "", article_title = "", abstract = "", cross_ref_data = ""):
        
        self.resource_type = resource_type
        self.website_title = website_title
        self.resource_title = resource_title
        self.url = url
        self.textual_content = textual_content
        self.resource_save_path = resource_save_path
        self.doi = doi
        self.article_title = article_title
        self.abstract = abstract
        self.cross_ref_data = cross_ref_data