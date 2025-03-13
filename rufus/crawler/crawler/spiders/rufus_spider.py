'''import scrapy
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
import re
import nltk

# Ensure nltk tokenizer is available
nltk.download('punkt')

class RufusSpider(scrapy.Spider):
    name = 'rufus'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com']

    # Limit the number of articles scraped
    max_articles = 10
    scraped_articles = 0

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        # Find and follow links to articles
        for link in response.css('a::attr(href)').getall():
            if self.scraped_articles >= self.max_articles:
                break  # Stop scraping when the limit is reached

            if link.startswith('/news') and 'bbc.com' not in link:
                link = response.urljoin(link)  # Convert relative URL to absolute

            if 'bbc.com/news' in link:
                self.scraped_articles += 1
                yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extract content from different possible article containers
        main_content = soup.find('article') or soup.find('div', {'class': 'ssrcss-uf6wea-RichTextComponentWrapper'})

        # Extract and clean text
        main_text = main_content.get_text(strip=True) if main_content else "No content found"
        cleaned_content = self.clean_text(main_text)

        # Extract named entities
        entities = self.extract_entities(cleaned_content)

        # Summarize the text
        summary = self.summarize_text(cleaned_content)

        yield {
            'title': response.css('title::text').get(default="No Title"),
            'content': cleaned_content,
            'entities': entities,
            'summary': summary
        }

    def clean_text(self, text):
        stop_words = {"the", "is", "in", "and", "of", "to", "a", "an", "that", "this", "it"}
        words = text.split()
        filtered_text = [word for word in words if word.lower() not in stop_words and word.isalpha()]
        return ' '.join(filtered_text)

    def extract_entities(self, text):
        return re.findall(r'\b[A-Z][a-z]*\b', text)

    def summarize_text(self, text):
        if not text.strip():  # Handle empty or whitespace-only text
            return "No summary available"

        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 3)
            return ' '.join(str(sentence) for sentence in summary)
        except Exception as e:
            return f"Summarization failed: {str(e)}"
'''
import scrapy
from bs4 import BeautifulSoup
from transformers import pipeline
import nltk
import spacy
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_fixed

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load NLP models
nlp = spacy.load('en_core_web_sm')
summarizer = pipeline('summarization')

class RufusSpider(scrapy.Spider):
    name = 'rufus'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com']  # Change this to real URLs

    # Define section keywords for selective scraping
    relevant_sections = ["faq", "pricing", "application", "contact", "support"]

    def parse(self, response):
        # Wrap the parsing logic in a try-except block for error handling
        try:
            soup = BeautifulSoup(response.body, 'html.parser')

            # Extract relevant sections dynamically
            extracted_sections = []
            for keyword in self.relevant_sections:
                section = soup.find(lambda tag: tag.name in ["div", "section", "article"] and keyword in tag.get_text().lower())
                if section:
                    extracted_sections.append(section.get_text())

            # Join extracted content
            main_content = " ".join(extracted_sections) if extracted_sections else soup.get_text()

            # Clean the text
            cleaned_content = self.clean_text(main_content)

            # Extract named entities
            entities = self.extract_entities(cleaned_content)

            # Summarize content
            summary = self.summarize_text(cleaned_content)

            # Structured output
            scraped_data = {
                "title": response.css('title::text').get(),
                "url": response.url,
                "content": cleaned_content,
                "entities": entities,
                "summary": summary,
                "scraped_date": response.headers.get('Date', b'').decode('utf-8')
            }

            # Save output as JSON
            with open("scraped_output.json", "w", encoding="utf-8") as file:
                json.dump(scraped_data, file, indent=4)

            yield scraped_data

        except Exception as e:
            self.logger.error(f"Error occurred during scraping: {e}")
            # Retry logic or fallback logic can be implemented here if needed
            return None

    def clean_text(self, text):
        """Remove stopwords and unnecessary words."""
        try:
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text)
            filtered_text = [word for word in words if word.lower() not in stop_words and word.isalpha()]
            return " ".join(filtered_text)
        except Exception as e:
            self.logger.error(f"Error occurred while cleaning text: {e}")
            return text

    def extract_entities(self, text):
        """Extract named entities using spaCy."""
        try:
            doc = nlp(text)
            return [(ent.text, ent.label_) for ent in doc.ents]
        except Exception as e:
            self.logger.error(f"Error occurred while extracting entities: {e}")
            return []

    def summarize_text(self, text):
        """Summarize text using Hugging Face Transformers."""
        try:
            if len(text.split()) > 1024:
                text = " ".join(text.split()[:1024])  # Limit text size to avoid transformer input issues
            summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            self.logger.error(f"Error occurred while summarizing text: {e}")
            return text  # Return original text if summarization fails

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))  # Retry 3 times with 5s delay
    def fetch_page_with_retry(self, url):
        """Fetch page with retry logic."""
        try:
            response = scrapy.Request(url)
            return response
        except RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            raise e  # Retry the request if it fails


