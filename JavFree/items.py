# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JavfreeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    view = scrapy.Field()
    actress = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    serie = scrapy.Field()
    image_urls = scrapy.Field()
    image = scrapy.Field()

