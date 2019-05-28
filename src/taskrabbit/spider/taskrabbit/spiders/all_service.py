import scrapy
import json
import uuid

from Taskrabbit.items import Cities, Query


class ServicesSpider (scrapy.Spider):
    """
    Retrieves all possible queries combinations. A query is a combination of a service and a particular location.
    """
    name = "all_service"
    start_urls = []
    with open('allqueries.json') as f:
        queries = json.load(f)

    for entry in queries:
        start_urls.append((entry['url']))
    #start_urls= ['https://www.taskrabbit.com/m/featured/delivery-service']
        def parse(self, response):
            for links in response.css('span.btn.btn-primary.btn-large.btn-fixed.js__formEntry'):
                 item = Query()
                 item['url'] = links.css('span::attr(data-path)').extract_first()
                 #queries['url'] = item['url']
                 if item['url']:
                    yield item
                    