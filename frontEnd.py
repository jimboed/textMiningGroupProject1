 
import flask
from sqlalchemy.orm import relationship
import flask_sqlalchemy
 
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String, Boolean

import os

from sqlalchemy.orm import scoped_session, sessionmaker

 
 
# >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> 
# spider def
# >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> 

 
 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from googlesearch import search 
import requests 
import scrapy
from scrapy.crawler import CrawlerRunner
# from scrapy.crawler import Crawler
 
# import requests
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from scrapy import signals
 


from scrapy.utils.project import get_project_settings

def submitQueryToSpider(company, terms):
	# t = terms.split(',')
	print()
	print()
	print("cd test1 && scrapy crawl test_spider -a company="+company+ " -a terms="+terms)
	print()
	print()
	os.system("cd test1 && scrapy crawl test_spider -a company="+company+ " -a terms="+terms)
	# # settings = get_project_settings()
	# crawler = CrawlerRunner()
	 
 

	# # 'followall' is the name of one of the spiders of the project.
	# crawler.crawl(TestSpiderSpider, domain='scrapinghub.com')
	# crawler.start() # the script will block here until the crawling is finished

def buildQuery(_company, _terms):
	# to search 

	company = _company

	startingKeywords =  _terms


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

	print(links)
	with open("links.txt", 'w') as tf:
		for x in links:
			tf.write(x+'\n')
	return links
 
 

# class TestSpiderSpider(scrapy.Spider):
# 	name = 'test_spider'
# 	start_urls = buildQuery("exxon", "fraud,indict,laundering")
	

# 	custom_settings = {'DEPTH_LIMIT': 3,}
 
# 	rules = (Rule(LinkExtractor(), callback='parse_item', follow=True),)
 
 




# 	def parse_item(self, response):
 

# 		filename = response.url.split("/")[-2] + '.html'
# 		with open(filename, 'wb') as f:
# 			f.write(response.body)
# 		txtfilename = response.url.split("/")[-2] + '.txt'
# 		with open(txtfilename, 'w') as tf:
# 			tf.write(str(response.xpath('//body//p//text()').extract()))

		

# <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< 
# <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< 



basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	# ...
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
 



app = flask.Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'joe'
db = flask_sqlalchemy.SQLAlchemy(app)
 

# app = flask.Flask(__name__)
# # app.config.from_pyfile('settings.py')
# app.config.from_object(Config)

 
# engine = create_engine('sqlite:///spiderQueries.db', echo=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#										  autoflush=False,
#										  bind=engine))
# Base = declarative_base()

# Base.metadata.create_all(engine)

# Base.query = db_session.query_property()
# Base.metadata.create_all(bind=engine)


# db = flask_sqlalchemy.SQLAlchemy(app) 

# db.init_app(app)



# >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> 
# >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> 
# MODELS
# <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< 
# <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< 

class SpiderQuery(db.Model):
	__tablename__ = 'hspiderqueries'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	company = db.Column( db.String(60) )
	terms = db.Column( db.String(61) )
	has_result = db.Column(db.Boolean, unique=False, default=False)

 
	def __init__(self,company, terms, has_result=False):
		self.company = company
		self.terms = terms
		self.has_result = has_result




# >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> 
# >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> 
# VIEWS
# <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< 
# <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< 
 

@app.route('/')
def hello():
	spiderQueries = SpiderQuery.query.all()

	spiderQueriesList = []
	for sQ in spiderQueries: spiderQueriesList.append( { sQ.id: {'company':sQ.company,  'terms': sQ.terms, 'has_result':sQ.has_result} } )
	print(spiderQueriesList)

	return flask.render_template("query.html", spiderQueriesList=spiderQueriesList)


@app.route('/submitQuery', methods=['POST'])
def submitQuery():
	print(flask.request.form)


	c = flask.request.form['company']
	t = flask.request.form['termsToMatch']

	# if flask.request.form['company'] and flask.request.form['termsToMatch']:
	# 	c = flask.request.form['company']
	# 	t = flask.request.form['termsToMatch']
	
	q = SpiderQuery.query.filter_by(company=c,terms=t ).first()
	
	if not q:
		newSpiderQuery = SpiderQuery(c,t,False)
		db.session.add(newSpiderQuery)
		db.session.commit()
	else:
		flask.flash('That query has already been submitted. ')

	submitQueryToSpider(c,t)

	return flask.redirect('/')

@app.route('/queryInfo/<company>/<terms>')
def queryInfo(company, terms):
	print("!!!!")
	print(company,'.')
	print(terms,'.')

	queryResults=[]
 
	q = SpiderQuery.query.filter_by(company=company,terms=terms ).first()

	if q.has_result == False:
		flask.flash('This query has not YET completed, ')
		flask.flash('check back again soon.')

	return flask.render_template("queryResult.html")






if __name__ == '__main__':
	db.create_all()
	app.run()
	 



