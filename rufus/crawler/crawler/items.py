import scrapy

class RufusItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    metadata = scrapy.Field()
