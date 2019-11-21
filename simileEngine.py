import nltk 
# nltk.download('wordnet')
from nltk.corpus import wordnet 

nltk.download('wordnet')

synonyms = [] 
antonyms = [] 

words = [ 'fraud', 
			'laundering',
			'trafficking',
			'indict',
			'scandal'


]

def synonymGetter(words):
	synonymDict = {}
	# antonymDict = {} 

	for word in words: 
		print('####### ', word)
		synonyms = [] 
		# antonyms = [] 
	
		for syn in wordnet.synsets(word): 
			for l in syn.lemmas(): 
				synonyms.append(l.name()) 
				# if l.antonyms(): 
				# 	antonyms.append(l.antonyms()[0].name()) 
		
		print('syns: ',set(synonyms)) 
		# print('ants: ',set(antonyms))

		if len(set(synonyms))>0:
			synonymDict[word] = set(synonyms)
		# if len(set(antonyms)) > 0:
		# 	antonymDict[word] = set(antonyms)
	print(synonymDict)
	return synonymDict


