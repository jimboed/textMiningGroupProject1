 
 
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
import os


 

class TestSpiderSpider(CrawlSpider):
	name = 'test_spider'
	 
	start_urls = []

	custom_settings = {
		'DEPTH_LIMIT': 1,
		'PAGES_PER_DOMAIN': 5
	}
 
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)
	company = ''
	terms = ''
	terms_name = ''
	path = ''
 
	def __init__(self, *args, **kwargs):
		super(TestSpiderSpider, self).__init__(*args, **kwargs) 
		print("-------- "+ kwargs.get('company') +' '+  kwargs.get('terms'))
		company = kwargs.get('company')
		terms  = kwargs.get('terms')

		for term in terms.split(','):
			self.terms_name = self.terms_name + '_'+ term

		self.path = 'corpus/'+company+'/'+self.terms_name+'/'
	
		if not os.path.exists(self.path):
			os.makedirs(self.path)

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
		requests.get('http://127.0.0.1:5000/callback/'+self.company+'/'+self.terms)



	def parse_item(self, response):
		print("######################################################################")
		print(response.meta['depth'])
		print("######################################################################")
		
		# time.sleep(1)
 
		filename = self.path+response.url.split("/")[-2] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		txtfilename = self.path+response.url.split("/")[-2] + '.txt'
		with open(txtfilename, 'w') as tf:
			tf.write(str(response.xpath('//body//p//text()').extract()))

	


	def buildQuery(self, _company, _terms):
		# to search 
		
		company = _company


		startingKeywords = _terms.split(',')

		print(company)
		print(startingKeywords)


		# query = '"exxon" (`fraud OR ~ lauder OR ~scandal OR ~indict)'
		query = '"'+company +'" (~'

		
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
		
		with open(self.path+"_links.txt", 'w') as tf:
			tf.write(query+'\n')
			for x in links:
				tf.write(x+'\n')
		return links
	