import scrapy
import json
import uuid

from taskrabbit.items import TaskRabbitCity, Query


class ServicesSpider (scrapy.Spider):
    """
    Retrieves all possible queries combinations. A query is a combination of a service and a particular location.
    """
    name = "services"

    start_urls = [
        'https://www.spider.co.uk/m/all-services'
    ]

    def parse(self, response):
        for task in response.css('.mg-panel__template-item'):
            item = Query()
            item['id'] = str(uuid.uuid4())
            item['task_title'] = task.css('a::text').extract_first()
            item['country'] = 'UK'
            item['url'] = task.css('a::attr(href)').extract_first()
            if item['task_title']:
                yield item
