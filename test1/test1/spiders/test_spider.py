 
 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from googlesearch import search 
import requests 
import scrapy
 
 
# import requests
 







def buildQuery(_company, _terms):
	# to search 

	company = _company


	startingKeywords = _terms.split(',')

	print(company)
	print(startingKeywords)


	# query = '"exxon" (`fraud OR ~ lauder OR ~scandal OR ~indict)'
	query = '"'+company +'" ('

	
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
 
 

class TestSpiderSpider(scrapy.Spider):
	name = 'test_spider'
	 
	 
	custom_settings = {
				'DEPTH_LIMIT': 30,
	}
 
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)
 
	def __init__(self, *args, **kwargs):
		super(TestSpiderSpider, self).__init__(*args, **kwargs) 
		print("-------- "+ kwargs.get('company') +' '+  kwargs.get('terms')
)
		company = kwargs.get('company')
		terms  = kwargs.get('terms')
		 


		self.start_urls = buildQuery(company,terms)
		




	def parse_item(self, response):
		print(self.start_urls)
		print(">>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> ")
		print(response)

		exit()
		filename = 'corpus/'+response.url.split("/")[-2] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		txtfilename = 'corpus/'+response.url.split("/")[-2] + '.txt'
		with open(txtfilename, 'w') as tf:
			tf.write(str(response.xpath('//body//p//text()').extract()))

		