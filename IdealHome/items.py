# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IdealhomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    create_at = scrapy.Field()
    apartment_name = scrapy.Field()
    floor = scrapy.Field()
    url = scrapy.Field()
    pass
