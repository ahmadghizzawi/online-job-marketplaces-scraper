import scrapy
from taskrabbit.items import TaskRabbitCity


class CitiesSpider(scrapy.Spider):
    name = "cities"
    start_urls = [
        'https://www.spider.com/',
    ]

    def parse(self, response):
        for city in response.css('section.static-section:not(.trhp__services-section) .exterior__bottom--md'):
            item = TaskRabbitCity()
            item['city'] = city.css('a::text').extract_first()
            item['url'] = city.css("a::attr(href)").extract_first()

            if item['city']:
                yield item
