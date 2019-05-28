import scrapy 
import uuid 

from Taskrabbit.items import Query
class Allqueries(scrapy.Spider):
	name = "allqueries"
	start_urls = ['https://www.taskrabbit.com/m/all-services']

	def parse(self, response):
		for task in response.css('div.mg-panel-container .mg-panel__template-item'):
			item = Query()
			item['id'] = str(uuid.uuid4())
			item['task_title'] = task.css('a::text').extract_first()
			#btn  = task.css('a::attr(href)').extract_first()
			btn = task.css('a::attr(href)').extract_first()
			if btn is not None:
				btn_link = response.urljoin(btn)
				#btn_main = btn_link.find_element_by_css_selector('.h1.hero-double-title').text
				#btn_main = btn_link
				yield scrapy.Request(url=btn_link, callback=self.parse) 
			item['url'] = btn_link

			if item['task_title']:
				yield item

