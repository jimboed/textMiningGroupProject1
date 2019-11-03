# -*- coding: utf-8 -*-
import scrapy


class TestSpiderSpider(scrapy.Spider):
	name = 'test_spider'
	allowed_domains = ['www.goodreads.com/quotes']
	start_urls = ['http://www.goodreads.com/quotes/']

	def parse(self, response):
		quotesDict = []
		selector = response.css('div.quoteDetails div.quoteText')
		for quote in selector:
			text = quote.css('::text').extract_first()
			author = quote.css('span::text').extract_first()
			combined = (text, author)
			quotesDict += [combined]
		self.write_as_html(quotesDict)
	
	def write_as_html(self, dict_items):
		htmlText = '''
		<html>
			<head><title>popular quotes</title></head>
			<body>{LINKS}</body>
		</html>
		'''
		link_items = '<ol>'

		for x in dict_items:
			link_items += f"<li>{x[0]} <span>{x[1]}</span></li>"
		link_items += '</ol>'
		htmlText = htmlText.format(LINKS=link_items)

		with open("spider1output.html", 'w') as file:
			file.write(htmlText)