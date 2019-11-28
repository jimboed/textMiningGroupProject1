# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:06:37 2019

@author: Rahul
"""

 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider2(CrawlSpider):
	name = 'nbcnews'
	allowed_domains = ['nbcnews.com']
	start_urls = ['https://www.nbcnews.com/business']
	

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