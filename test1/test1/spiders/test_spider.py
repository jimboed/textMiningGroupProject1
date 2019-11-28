 
 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from googlesearch import search 
import requests 
import scrapy
from scrapy.crawler import CrawlerProcess
 
# import requests
 







def buildQuery():
	# to search 

	company = "exxon"

	startingKeywords = [ 	'fraud', 
							'launder',
							'scandal', 
							'indict'

	]


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

	print(links)
	with open("links.txt", 'w') as tf:
		for x in links:
			tf.write(x+'\n')
	return links
 
 

class TestSpiderSpider(scrapy.Spider):
	name = 'test_spider'
	start_urls = buildQuery()
	

	custom_settings = {
        'DEPTH_LIMIT': 3,
	}
 
	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)
 
 




	def parse_item(self, response):
 

		filename = response.url.split("/")[-2] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
		txtfilename = response.url.split("/")[-2] + '.txt'
		with open(txtfilename, 'w') as tf:
			tf.write(str(response.xpath('//body//p//text()').extract()))

		