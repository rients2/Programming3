"""citation_graph.py: this file uses the pickles with the pubmedids, references and keywords to create a citation graph"""

import glob
import pickle
import numpy as np
import pandas as pd
import networkx as nx
import dask.dataframe as dd

pickle_path2 = '/students/2021-2022/master/Rients_DSLS/pickle_frames/'
pickles = glob.glob(pickle_path2 + 'pubmed21n*.pkl')

# Creating a dataframe that has all the authors and their corresponding paper.
# Using dask
ddf2 = dd
ddf_list = []

# small frame
pickles = pickles[:1]

for pickle in pickles:
    # Creating a pandas dataframe from each pickle
    df = pd.read_pickle(pickle)

    # Turning pandas df into a dask dataframe.
    ddf = dd.from_pandas(df, npartitions=8)
    ddf_list.append(ddf)   
    nr = len(ddf_list)
    print('list size: ', nr, '/1062')

print('Combining dataframes. ETA: ~20 sec')
full_frame = dd.multi.concat(ddf_list)
# ~2 min


# Creating a citation graph with a list keywords as node attribute.
# Using the full dask dataframe

full_frame_refs = full_frame[full_frame['Refs'].isna() == False]
# Creating a citation graph
cite_graph = nx.Graph()

# change keywords to Authors to get the authors as attributes
for l, p, k in zip(full_frame_refs['pubmedID'], full_frame_refs['Refs'], full_frame_refs['keywords']):
    try:
        cite_graph.add_node(l, keywords=k)
    except:
        print('Error')
    for p2 in p:
        cite_graph.add_edge(l,p2)


# Writing the graph to a pickle file.
#nx.write_gpickle(cite_graph, path='/students/2021-2022/master/Rients_DSLS/pickle_graph/cite_graph.pkl')

nx.write_gpickle(cite_graph, path='/students/2021-2022/master/Rients_DSLS/pickle_graph/cite_small.pkl')

