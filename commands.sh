#!/bin/bash


# # open shell interface
# scrapy shell www.goodreads.com



# # create projcet called "test1"
# scrapy startproject test1



# # create spider 
# # scrapy genspider <name of spider> < url to start from >
# cd test1 
# scrapy genspider test_spider www.goodreads.com/quotes 
# cd .. 


# crawl
# scrapy crawl <spider>











 
cd test1 
# nohup scrapy crawl test_spider -a company=exxon -a terms=fraud,embezzle,launder 
scrapy crawl test_spider -a company=exxon -a terms=fraud,embezzle,launder 
# scrapy crawl nbcnews

cd ..








# python3 googleSearch2.py