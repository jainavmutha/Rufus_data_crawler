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
from scrapy.http import HtmlResponse
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
import spacy
import re
import nltk

# Ensure necessary resources are available
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")  # Load spaCy English NLP model

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

        # Extract named entities using spaCy
        entities = self.extract_entities(cleaned_content)

        # Summarize the text using TextRank
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
        """
        Use spaCy for Named Entity Recognition (NER)
        Extract and return unique named entities (e.g., people, places, organizations).
        """
        doc = nlp(text)
        entities = set()  # Use a set to avoid duplicates
        for ent in doc.ents:
            entities.add(ent.text)
        return list(entities)

    def summarize_text(self, text):
        """
        Summarize the text using the TextRank algorithm from sumy.
        """
        if not text.strip():
            return "No summary available"

        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = TextRankSummarizer()  # Use TextRank instead of LSA
            summary = summarizer(parser.document, 3)  # Extract 3 sentences
            return ' '.join(str(sentence) for sentence in summary)
        except Exception as e:
            return f"Summarization failed: {str(e)}"
