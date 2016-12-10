# Libraries
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import codecs
import networkx as nx
import seaborn as sns
sns.set()

################################################################################
################################################################################
# Functions

def de_gutenberger(filename):
    # Gets rid of the Gutenberg header and footer crap
    

    f = codecs.open(filename, "r", encoding='utf-8')
    data = f.readlines()
    f.close()

    for index1, value1 in enumerate(data):
        if u"START OF THIS PROJECT GUTENBERG" in value1:
            break

    for index2, value2 in enumerate(data):
        if u"END OF THIS PROJECT GUTENBERG" in value2:
            break

    if index1 == index2:
        index1 = 0
        index2 = len(data)

    output_string = ""
    for i in data[index1:index2-1]:
        output_string += i

    return nltk.word_tokenize(output_string)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def word_prep2(input_word):
    # Prepares a text: stems, and gets rid of stop words.

    try:
        empty_string = ""
        for i in input_word:
            if i not in stop_list:
                empty_string += " " + stemmer.stem(i.lower())

        return empty_string
    except Exception, e:
        print str(e)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def get_authors(files):
    # Get the authors from each text file.

    authors = []

    for index, i in enumerate(files):

        filename = folder + i

        f = codecs.open(filename, "r", encoding='utf-8')
        data = f.readlines()
        f.close()

        known = False
        for index1, value1 in enumerate(data):
            if "Author: " in value1:
                authors.append(value1)
                known = True
                break

        if known == False:
            authors.append("Unknown")

    return authors

# stemmer and stop_list objects for use in above functions
stemmer = PorterStemmer()
stop_list = stopwords.words('english') + list(string.punctuation)
stop_list = [str(x) for x in stop_list]
# add a list of bullshit punctuation to stop words list
stop_list.extend([",--", ',"--', ',--', '?"--', ".--", "--", '"', '."--', '?--', '!--', "?-", ";--", 
            '--"', '.--"', ',"', '?"', '."', '!"', '!"--', ';"', '--`', ".'--", ".'", ";'", ",'", 
            "!'", ".)", "),", ":--", "\n", '``', "'d", "''", "'s"])

# Location of texts
folder = "/home/blake/Drive/Other/GITHUB/Book_Analysis/texts/"
files = os.listdir(folder)
master = []
authors = get_authors(files)

# Sort the texts by author alphabetically
from operator import itemgetter
authors, files = (list(x) for x in zip(*sorted(zip(authors, files),key=itemgetter(0))))

# Loop over files, add processed text to master list
for index, i in enumerate(files):
    print index, i
    filename = folder + i

    a = de_gutenberger(filename)

    b = word_prep2(a)
    master.append(b)


# Apply TfidfVect
print "attempting TfidfVect"
vect = TfidfVectorizer(min_df=1, max_df = 1.0)
tfidf = vect.fit_transform(master)

# vari is the covariance matrix
vari = (tfidf * tfidf.T).A
print vari

# For use with plotting perhaps:
author_label = [x.split("Author: ")[-1][:-1] for x in authors]

################################################################################
################################################################################
# Plotting

# Heatmap first
fig1 = figure(1)
ax1 = subplot(111)

clf()
ax1.set_aspect('auto')
pcolor(vari, cmap = "Greys")

xticks(arange(70) + 0.5, author_label, rotation = 90)
yticks(arange(70) + 0.5, author_label)
show()

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

# Now for the minimal spanning tree plot
# Turn covariance matrix into 'distance' matrix:
dij = np.nan_to_num(np.sqrt(2*(1-vari)))

# Make networkx graph object
G = nx.from_numpy_matrix(dij)

# Make minimum spanning tree
T = nx.minimum_spanning_tree(G)
position = nx.spring_layout(T)


plt.figure(2)
ax2 = subplot(111)

plt.clf()

ax2.set_aspect('auto')
nx.draw(T, pos=pos2, with_labels=True, node_size = 1200)
plt.show()
