from prompt_processing import extract_info_from_prompt
from crawler.crawler.spiders.rufus_spider import RufusSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider_with_prompt(instructions):
    # Extract domain and relevant sections from the prompt
    domain, relevant_sections = extract_info_from_prompt(instructions)
    
    # Set up Scrapy crawler process
    process = CrawlerProcess(get_project_settings())

    # Start the spider with dynamic parameters
    process.crawl(RufusSpider, domain=domain, relevant_sections=relevant_sections)
    
    # Start the spider
    process.start()

# Example of using the function with a prompt
instructions = "We're making a chatbot for the HR in San Francisco."
run_spider_with_prompt(instructions)
