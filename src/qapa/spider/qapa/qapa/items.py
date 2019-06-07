# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QapaCities(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()

class QapaQuery(scrapy.Item):
	id = scrapy.Field()
	task_title = scrapy.Field()
	city = scrapy.Field()
	url = scrapy.Field()
