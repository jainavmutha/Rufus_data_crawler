from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse

class SeleniumMiddleware:
    def __init__(self):
        self.driver = webdriver.Firefox()  # Or use Chrome

    def process_request(self, request, spider):
        self.driver.get(request.url)
        body = self.driver.page_source
        return HtmlResponse(url=request.url, body=body, encoding="utf-8", request=request)
    
    def __del__(self):
        self.driver.quit()
