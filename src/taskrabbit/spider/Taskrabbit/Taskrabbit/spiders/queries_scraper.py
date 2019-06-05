import scrapy
import json
import uuid

from Taskrabbit.items import Cities, Query


class QueriesSpider(scrapy.Spider):
    """
    Retrieves all possible queries combinations. A query is a combination of a service and a particular location.
    """
    name = "queries"

    def start_requests(self):
        with open('cities.json') as f:
            cities = json.load(f)

        main_url = 'https://www.taskrabbit.com'
        start_urls = []

        for entry in cities:
            start_urls.append((main_url + entry['url'], entry['city']))

        for entry in start_urls:
            yield scrapy.Request(entry[0], meta={'city': entry[1]})

    def parse(self, response):
        for task in response.css('#metro-templates .mktg-template-item'):
            item = Query()
            item['id'] = str(uuid.uuid4())
            item['task_title'] = task.css('.mktg-template-item--title-link::text').extract_first()
            item['city'] = response.meta['city']
            item['url'] = task.css('.btn.btn-secondary.btn-small.js__formEntry::attr(data-path)').extract_first()

            if item['task_title']:
                yield item
