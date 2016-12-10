import os
import re
import nltk
import string
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


def de_gutenberger(filename):
	
	#read in 
	with open(filename, 'r') as f:
		txt = f.read()

	author, title = get_author_and_title(txt)

	# get rid of header & footer
	start_txt = "START OF THIS PROJECT GUTENBERG EBOOK"
	end_txt	  = "END OF THIS PROJECT GUTENBERG EBOOK"

	start = re.search('('+start_txt+').*?\n', txt)
	start_ind = start.end() if start != None else 0
		
	end = re.search('('+end_txt+').*?\n', txt)
	end_ind = end.start() if end != None else len(txt)

	word_string = stem_and_stop(nltk.word_tokenize(txt[start_ind:end_ind])) 

	return author, title, word_string

def get_author_and_title(txt):
	
	name_search = re.search('(?<=Author: ).*?\n', txt)
	name = 'Unknown' if name_search == None else name_search.group()[:-1]
	
	title_search = re.search('(?<=Title: ).*?\n', txt)
	title = 'Unknown' if title_search == None else title_search.group()[:-1]
	
	return name, title


def stem_and_stop(words):

	stemmer = PorterStemmer()
	stop_list = stopwords.words('english') + list(string.punctuation)
	stop_list = [str(x) for x in stop_list]

	# add a list of bullshit punctuation to stop words list
	stop_list.extend([",--", ',"--', ',--', '?"--', ".--", "--", '"', 
		'."--', '?--', '!--', "?-", ";--", 
            	'--"', '.--"', ',"', '?"', '."', '!"', '!"--', 
		';"', '--`', ".'--", ".'", ";'", ",'", 
            	"!'", ".)", "),", ":--", "\n", '``', "'d", "''", "'s"])


	empty_string = ""
	for word in words:
		if word not in stop_list:
			empty_string += " " + stemmer.stem(word.lower())

	return empty_string


def get_books(folder, files): 

	authors = []
	texts   = []
	titles  = []
	for i, f in enumerate(files):
		print("Number {} of {}".format(i+1, len(files))) 

		author, title, txt = de_gutenberger(folder + f)
		authors.append(author)
		titles.append(title)
		texts.append(txt)
		break	
	return authors, titles, texts	

def do_tfidf(texts):

	vect = TfidfVectorizer(min_df=1, max_df = 1.0)
	tfidf = vect.fit_transform(texts)

	vari = (tfidf * tfidf.T).A
	return tfidf

if __name__ == '__main__':

	folder = "data/"
	files = os.listdir(folder)

	authors, titles, texts = get_books(folder, files)

	dist_mat = do_tfidf(texts)
