BOT_NAME = 'rufus'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 5
RETRY_ENABLED = True
RETRY_TIMES = 3

# Enable logging for debugging
LOG_LEVEL = 'DEBUG'

# Add settings for output
FEED_FORMAT = 'json'
FEED_URI = 'output.json'
