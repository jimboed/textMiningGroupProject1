 
 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from googlesearch import search 
import requests 
import scrapy
import time
 
 
# import requests
 
from scrapy import signals
from scrapy import Spider



 

class TestSpiderSpider(CrawlSpider):
	name = 'test_spider'
	 
	start_urls = []

	custom_settings = {
		'DEPTH_LIMIT': 1
	}
 
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)
 
	def __init__(self, *args, **kwargs):
		super(TestSpiderSpider, self).__init__(*args, **kwargs) 
		print("-------- "+ kwargs.get('company') +' '+  kwargs.get('terms'))
		company = kwargs.get('company')
		terms  = kwargs.get('terms')
		self.start_urls = self.buildQuery(company,terms)
  


	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(TestSpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider



		
	def spider_closed(self, reason):
		# with open("spiderTracker.txt", 'w') as f:
		# 	f.write('doneCrawling')

		print("DONEZO!!!!!")



	def parse_item(self, response):
		print("######################################################################")
		print(response.meta['depth'])
		print("######################################################################")
		
		# time.sleep(1)
 
		filename = 'corpus/'+response.url.split("/")[-2] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		txtfilename = 'corpus/'+response.url.split("/")[-2] + '.txt'
		with open(txtfilename, 'w') as tf:
			tf.write(str(response.xpath('//body//p//text()').extract()))

	


	def buildQuery(self, _company, _terms):
		# to search 
		
		company = _company


		startingKeywords = _terms.split(',')

		print(company)
		print(startingKeywords)


		# query = '"exxon" (`fraud OR ~ lauder OR ~scandal OR ~indict)'
		query = '"'+company +'" (~ '

		
		# build query
		for i, keyword in enumerate(startingKeywords):
			query +=  " " + keyword
			if i < len(startingKeywords) -1:
				query +=  " OR ~"
			

		query += ")"

		links = []
		
		# get links
		for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
			links.append(j)

		print(query)
		print(links)
		
		with open("corpus/links.txt", 'w') as tf:
			tf.write(query+'\n')
			for x in links:
				tf.write(x+'\n')
		return links
	