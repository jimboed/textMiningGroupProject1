import requests
from urllib.request import Request, urlopen

from googlesearch import search 


# import requests
from bs4 import BeautifulSoup


thesaurus = 'https://www.powerthesaurus.org/'

query = 'fraud'
adjustedQuery = thesaurus

queryPieces = query.split(' ')
print(queryPieces)
for q in queryPieces:
	if len(adjustedQuery) > 0:
		adjustedQuery = adjustedQuery+'_'+q
	else: 
		adjustedQuery = q
adjustedQuery+='/synonyms'
print(adjustedQuery)

print(thesaurus+adjustedQuery+'/synonyms')
response = requests.get(thesaurus+adjustedQuery+'/synonyms')

req = Request(adjustedQuery, headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read()
# print(webpage)
# print(response.text)



soup = BeautifulSoup(webpage, 'html.parser')
text = soup.find_all(text=True)

output = ''
blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	"style",
	"[if lt IE 9]>"
	# there may be more elements you don't want, such as "style", etc.
]

for t in text:
	if t.parent.name not in blacklist:
		output += '{} '.format(t)

print(output)









 





# for j in search(query, tld="co.in", num=10, stop=20, pause=2): 
#     print(j) 







url = 'https://www.troyhunt.com/the-773-million-record-collection-1-data-reach/'
res = requests.get(url)
html_page = res.content

soup = BeautifulSoup(html_page, 'html.parser')
text = soup.find_all(text=True)

output = ''
blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	# there may be more elements you don't want, such as "style", etc.
]

for t in text:
	if t.parent.name not in blacklist:
		output += '{} '.format(t)

print(output)