import scrapy
import json
import uuid

from Taskrabbit.items import Query


class ServicesSpider (scrapy.Spider):
    name = "final"
    start_urls = []
    with open('allqueries.json') as f:
        queries = json.load(f)

    for entry in queries:
        start_urls.append(entry['url'])
        def parse(self, response):
            for links in response.css('div.container.stretch-height'):
                item = Query()
                item['id'] = str(uuid.uuid4())
                item['task_title'] = links.xpath('/html/body/div[4]/div[2]/div[2]/div/section[1]/div/div/div/span[3]/a/span/text()').get()
                item['url'] = links.css('span::attr(data-path)').extract_first()

                if item['url']:
                    yield item
                    