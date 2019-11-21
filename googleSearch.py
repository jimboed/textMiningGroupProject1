from googlesearch import search 
import requests 
 
 
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

# crawl links

results = {}

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	'style',
	'img',
	"[if lt IE 9]>"
	# there may be more elements you don't want, such as "style", etc.
]

for url in links: 
	print(url)
	holdresults = []
	output = ''
	res = requests.get(url)
	html_page = res.content

	soup = BeautifulSoup(html_page, 'html.parser')
	text = soup.find_all(text=True)
	for t in text:
		if t.parent.name not in blacklist:
			output += '{} '.format(t)
	results[url] = output

print()
print()
print()

print(results)

with open("z_results.txt", 'w') as f:
	for url, result in results.items(): 
		f.write("\n#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### \n")
		f.write(url)
		f.write("\n#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### \n")
		f.write(result)
		f.write("\n")


print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()



# url ="https://www.bloomberg.com/search?query=exxon%20fraud"

# res = requests.get(url)
# html_page = res.content


# soup = BeautifulSoup(html_page, 'html.parser')
# text = soup.find_all(text=True)
# for t in text:
# 	if t.parent.name not in blacklist:
# 		output += '{} '.format(t)
# print(output)
