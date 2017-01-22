# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# class GuokeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

class ScientificItem(scrapy.Item):
    label = scrapy.Field()
    subLabel = scrapy.Field()
    title = scrapy.Field()
    publishDate = scrapy.Field()
    summary = scrapy.Field()
    articleId = scrapy.Field()
    articleUrl = scrapy.Field()
