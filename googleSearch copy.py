from googlesearch import search 
import requests 
import scrapy
from scrapy.crawler import CrawlerProcess
 
# import requests
from bs4 import BeautifulSoup





 
  
 

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
print(query)
links = []
 
# get links
for j in search(query, tld="co.in", num=10, stop=20, pause=2): 
	links.append(j)

print(links)
 
 