"""question5.py: this file answers question nr 5."""
import csv
import numpy as np
import networkx as nx

cite_graph = nx.read_gpickle('/students/2021-2022/master/Rients_DSLS/pickle_graph/cite_graph.pkl')

# Loading all the subgraphs.
loaded_components = sorted(nx.connected_components(cite_graph), key=len, reverse=True)
# In total 727593 different subgraphs exist. 
total_cc = len(loaded_components)
# Making a subgraph of only the largest component.
cite_sg0 = cite_graph.subgraph(loaded_components[0])


matches = []
no_matches = []
amount_nodes = len(cite_sg0.nodes())
nodes_list = list(cite_sg0.nodes())


for n1, n2, k in list(cite_sg0.edges(data=True)):
    # Only check if they both have keywords.
    if cite_sg0.nodes[n1] != {} and cite_sg0.nodes[n2] != {}:
        #print(' node1: ', cite_sg0.nodes[n1]['keywords'],'\n', 'node2: ', cite_sg0.nodes[n2]['keywords'], '\n')
        key1 = cite_sg0.nodes[n1]['keywords']
        key2 = cite_sg0.nodes[n2]['keywords']
        matches.append(len(set(key1).intersection(key2)) / max(len(set(key1)),len(set(key2))))

cited_ans = int(np.mean(matches)*100)
print('The mean of shared keywords when there is a match: ', cited_ans)

# Checking the % of keywords that match when there is no citation. 
# I calculate this by just taking two random papers and checking them for matching keywords.
# By random chance there could be citations included, however unless it happens a 100+ times, it will not have an effect.
# And while I could prevent this, I dont want to add a lot of processing time.

for n in range(0,25000):
    n1 = nodes_list[np.random.randint(0,amount_nodes)]
    n2 = nodes_list[np.random.randint(0,amount_nodes)]

    # Incase both n1 and n2 end up being the same
    while n1 == n2:
        n2 = nodes_list[np.random.randint(0,amount_nodes)]
        #print('What are the odds.')
        
    if cite_sg0.nodes[n1] != {} and cite_sg0.nodes[n2] != {}:
        n_key1 = cite_sg0.nodes[n1]['keywords']
        n_key2 = cite_sg0.nodes[n2]['keywords']
        no_matches.append(len(set(n_key1).intersection(n_key2)) / max(len(set(n_key1)),len(set(n_key2))))

non_cite_ans = int(np.mean(no_matches)*100)
print('The mean of shared keywords of two random papers: ', non_cite_ans)


# Writing the answers.
with open('/homes/rdalstra/Documents/Programming3/Assignment6/answers.csv', mode='w') as csv_file:
    answer_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    answer_writer.writerow(['Is there a correlation between citations and the number of keywords that papers share?', \
    'Yes ' + str(cited_ans) + '% is significantly different than ' + str(non_cite_ans)+ '%'])