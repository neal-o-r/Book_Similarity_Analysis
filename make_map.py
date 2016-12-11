import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from sklearn.manifold import TSNE
from bokeh_scatter import *
from books import *


def embed(dist, clusters, authors, titles):

       
	x = clusters + 0.5*np.random.rand(len(clusters)) - 0.25
	y = 10*np.random.rand(len(titles))

	d = {'Author':authors, 'Title':titles, 'Cluster':clusters,
		'X':x, 'Y':y}
        
	return pd.DataFrame(d)


if __name__ == '__main__':

	folder = "odata/"
	files = os.listdir(folder)

	authors, titles, texts = get_books(folder, files)

	clusters, mat = get_clusters_and_dists(texts)
	
	df = embed(mat, clusters, authors, titles)

	bokeh_scatter(df)

