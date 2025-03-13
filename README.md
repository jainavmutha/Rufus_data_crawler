# Rufus Spider: Web Scraping, Summarization, and Data Synthesis

**Rufus Spider** is a web scraping tool built using **Scrapy**, **spaCy**, and **Hugging Face Transformers**. It focuses on **selective scraping**, cleaning and summarizing the extracted content, and synthesizing structured documents in **JSON** format. The goal is to extract relevant data (e.g., FAQs, pricing, application forms) from websites and process it for use in **Retrieval-Augmented Generation (RAG)** systems or other applications.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Example Output](#example-output)
- [Customizing for Your Use Case](#customizing-for-your-use-case)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

Rufus Spider is designed to:

- **Selectively scrape relevant sections** of a webpage (e.g., FAQs, pricing, application forms).
- **Clean and process the text** by removing stopwords and unnecessary ads.
- **Extract named entities** (e.g., company names, dates) using **spaCy**.
- **Summarize the extracted content** using a **pre-trained Hugging Face Transformer model**.
- **Synthesize the scraped content** into a structured **JSON format** for use in downstream systems like **RAG**.

---

## Features

- **Selective Scraping**: Focuses on specific content like FAQs, pricing, and application forms.
- **Data Cleaning**: Removes irrelevant words, ads, and stopwords.
- **Named Entity Recognition (NER)**: Extracts key entities from the content (e.g., organization names, dates).
- **Summarization**: Condenses the content into a summary using **BART** or **DistilBERT** from Hugging Face.
- **Structured Output**: Saves the processed data as a **JSON** document, ideal for integration into RAG systems.

---

## Requirements

To run the project, ensure that you have the following dependencies installed:

- **Python 3.x**
- **Scrapy**: For web scraping.
- **spaCy**: For Natural Language Processing and Named Entity Recognition.
- **Hugging Face Transformers**: For text summarization.
- **NLTK**: For tokenization and stopword removal.
- **BeautifulSoup**: For HTML parsing.

You can install the necessary libraries by running:

```bash

pip install scrapy spacy transformers nltk beautifulsoup4
Installation
1. Install Dependencies
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv rufus
source rufus/bin/activate  # On Windows, use `rufus\Scripts\activate`
Then, install the required libraries:

bash
Copy
Edit
pip install scrapy spacy transformers nltk beautifulsoup4
2. Download the spaCy Model
Download the en_core_web_sm model for spaCy:

bash
Copy
Edit
python -m spacy download en_core_web_sm
3. Download NLTK Resources
Download necessary NLTK resources for tokenization and stopwords:

bash
Copy
Edit
import nltk
nltk.download('punkt')
nltk.download('stopwords')
Usage
1. Create the Spider
Create a file named rufus_spider.py and paste the Rufus Spider code from above.

2. Set the Start URL and Domain
In the RufusSpider class, modify the allowed_domains and start_urls to the target website(s) for scraping.

python
Copy
Edit
allowed_domains = ['bbc.com']  # Replace with the desired domain
start_urls = ['https://www.bbc.com']  # Replace with the starting URLs
3. Run the Spider
To run the spider and output the results to a JSON file, use the following command:

bash
Copy
Edit
scrapy crawl rufus -o output.json
This will start scraping the website(s) and store the extracted and processed data in output.json.

Code Explanation
parse Method
The main entry point of the spider:

It scrapes the page and parses the content using BeautifulSoup.
Extracts relevant sections (FAQ, pricing, etc.) using selective scraping.
Cleans the content by removing unnecessary words, stopwords, and ads.
Extracts named entities from the cleaned text using spaCy.
Summarizes the content using Hugging Face Transformers.
Outputs the processed data in JSON format.
clean_text Method
This method:

Tokenizes the text using NLTK's word tokenizer.
Filters out stopwords (common words that don't add value, like "the", "is", etc.).
Removes non-alphabetical tokens.
Adds a custom ad-filtering step to remove common ad-related phrases (e.g., "buy now").
extract_entities Method
Uses spaCy to process the text and extract named entities such as:

Person names (e.g., "John Doe")
Organizations (e.g., "Apple Inc.")
Dates (e.g., "January 2024")
summarize_text Method
Uses Hugging Face's pre-trained transformer model to generate a summary of the extracted content. This method also ensures the content isn't too long to be processed by the model.

Customizing for Your Use Case
1. Change Relevant Sections
You can modify the relevant_sections list to include other keywords or adjust the HTML tag types to better match the structure of the target website.

python
Copy
Edit
relevant_sections = ["about", "services", "contact", "team"]
2. Differentiate Ad-Filtering Logic
You can update the ad_keywords list in the clean_text method to filter additional unwanted phrases or words.

python
Copy
Edit
ad_keywords = ['sponsored', 'buy now', 'limited time offer']
3. Add Additional Summarization Models
If you want to use a different summarization model from Hugging Face, you can modify the summarizer pipeline to load another model.

python
Copy
Edit
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
Troubleshooting
1. spaCy Model Not Found
If you encounter an error like Can't find model 'en_core_web_sm', try re-downloading the spaCy model:

bash
Copy
Edit
python -m spacy download en_core_web_sm

2. Missing Dependencies
If you get errors about missing libraries, ensure you have installed the required packages:

bash
Copy
Edit
pip install scrapy spacy transformers nltk beautifulsoup4
3. Issues with JSON Output
Ensure that the JSON output is being written correctly by verifying the file permissions and path.

python
Copy
Edit

with open("scraped_output.json", "w", encoding="utf-8") as file:
    json.dump(scraped_data, file, indent=4)

Conclusion
Rufus Spider is a versatile tool for selectively scraping web content, cleaning and summarizing it, and producing structured output in JSON format. This can be useful for data analysis, RAG systems, or any other application that requires processed and structured web content.

Feel free to modify and extend the spider to suit your needs, and integrate it into your projects for more powerful data extraction and processing workflows.
