import os
import re
import nltk
import string
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import numpy as np
from sklearn.neighbors import DistanceMetric


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
	
	return authors, titles, texts	

def get_matrix(texts):

	vectorizer = TfidfVectorizer(max_df=0.5, min_df=2,
                                 use_idf=True, sublinear_tf=True)

	tfidf = vectorizer.fit_transform(texts)
	# get covariance
	vari = (tfidf * tfidf.T).A

	svd = TruncatedSVD(100, random_state=123)
	normalizer = Normalizer(copy=False)
	lsa = make_pipeline(svd, normalizer)

	X = lsa.fit_transform(tfidf)

	return X


def get_clusters_and_dists(texts):

	dense_matrix = get_matrix(texts)

	km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1)
	
	km.fit(dense_matrix)

	clusters = km.labels_

	dist = DistanceMetric.get_metric('manhattan')

	dist_mat = dist.pairwise(dense_matrix)

	return clusters, dist_mat

if __name__ == '__main__':

	folder = "data/"
	files = os.listdir(folder)

	authors, titles, texts = get_books(folder, files)

	clusters, dist_mat = get_clusters_and_dists(texts)
