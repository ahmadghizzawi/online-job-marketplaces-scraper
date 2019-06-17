import scrapy
from mistertemp.items import Cities


class CitiesSpider(scrapy.Spider):
    name = "cities"
    start_urls = ["https://www.mistertemp.com/interim/villes/"]

    def parse(self, response):
        for city in response.css("a.city-link"):
            item = Cities()
            item["city"] = city.css("a::text").extract_first()
            item["url"] = city.css("a::attr(href)").extract_first()

            if item["city"]:
                yield item
