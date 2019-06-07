# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Cities(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()

class Query(scrapy.Item):
    id = scrapy.Field()
    task_title = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()

class Worker(scrapy.Item):
    id = scrapy.Field()
    ranking = scrapy.Field()
    picture = scrapy.Field()
    positive_rating = scrapy.Field()
    number_of_relevant_tasks = scrapy.Field()
    great_value_badge = scrapy.Field()
    elite_tasker = scrapy.Field()
    new_tasker = scrapy.Field()
    how_can_help = scrapy.Field()
    right_person = scrapy.Field()
    when_tasking = scrapy.Field()
    number_of_reviews_received = scrapy.Field()
    per_hour_rate = scrapy.Field()
    query = scrapy.Field()
