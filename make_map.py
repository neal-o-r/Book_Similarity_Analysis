import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from sklearn import manifold
from bokeh_scatter import *
from books import *


def embed(dist, clusters, authors, titles):

        seed = 123

        mds = manifold.MDS(n_components=2, 
                max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)

        pos = mds.fit(dist).embedding_     
        
        d = {'Author':authors, 'Title':titles, 'Cluster':clusters,
		'X':pos[:,0], 'Y':pos[:,1]}
        
        return pd.DataFrame(d)

if __name__ == '__main__':


	folder = "data/"
	files = os.listdir(folder)

	authors, titles, texts = get_books(folder, files)

	clusters, dist_mat = get_clusters_and_dists(texts)
	
	df = embed(dist_mat, clusters, authors, titles)

	bokeh_scatter(df)

