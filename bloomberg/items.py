# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BloombergItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()
    pass
