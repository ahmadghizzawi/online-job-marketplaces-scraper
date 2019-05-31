import scrapy
from Taskrabbit.items import Cities


class CitiesSpider(scrapy.Spider):
    name = "cities"
    start_urls = [
        'https://www.taskrabbit.com/',
    ]

    def parse(self, response):
        for city in response.css('section.static-section:not(.trhp__services-section) div'):
             item = Cities() 
             item['city'] = city.css('a::text').extract_first()
             item['url'] = city.css("a::attr(href)").extract_first()

             if item['city']:
                 yield item
