"""author_paper_graph.py: this file uses the pickles with the pubmedids and authors to create an author-paper graph."""

import glob
import pickle
import numpy as np
import pandas as pd
import networkx as nx

pickle_path = '/students/2021-2022/master/Rients_DSLS/pickle_6/'
pickles = glob.glob(pickle_path + 'pubmed21n*.pkl')

# Creating a bipartite graph of papers and authors.
# Using networkx
full_graph = nx.Graph()
nr = 0
for pickle in pickles:
    # Creating a pandas dataframe from each pickle
    df = pd.read_pickle(pickle)
    nr += 1 
    # Creating 1 graph from the dataframe.
    for l, p in zip(df[0],df[1]):
        full_graph.add_edge(l,p)
    print('Added nodes to graph', nr)


# Creating a 4.3 gb graph.
#nx.write_gpickle(full_graph, path='/students/2021-2022/master/Rients_DSLS/pickle_graph/full_graph.pkl')
#~ 11 min


loaded_components = sorted(nx.connected_components(full_graph), key=len, reverse=True)
loaded_sg0 = full_graph.subgraph(loaded_components[0])

# Creating another 4.5gb graph. 
# Weirdly enough 200mb larger than the complete graph.
# Using pickle is the most efficient.
nx.write_gpickle(loaded_sg0, path='/students/2021-2022/master/Rients_DSLS/pickle_graph/full_sg.pkl')
# ~5 min