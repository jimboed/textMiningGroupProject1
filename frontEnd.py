 
import flask
from sqlalchemy.orm import relationship
import flask_sqlalchemy
 
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String, Boolean

import os

from sqlalchemy.orm import scoped_session, sessionmaker
import subprocess
 
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
 
# import thread
 
import threading
from scrapy.utils.project import get_project_settings

def submitQueryToSpider(company, terms):
	# t = terms.split(',')
	print()
	print()
	print("cd test1 && scrapy crawl test_spider -a company="+company+ " -a terms="+terms + " &>submitQuery.log")
	print()
	print()
	command = "cd test1 && scrapy crawl test_spider -a company="+company+ " -a terms="+terms+ " >> submitQuery.log 2>&1 &"
	# p = subprocess.Popen(["cd", "test1", "&&", "scrapy", "crawl" , "test_spider", "-a", "company=", company , "-a", "terms=",terms])
	
	# t = threading.Thread(target=os.system(command))
	# t.start()
	os.system(command)
	 
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
	app.run(port=5000)
	 



