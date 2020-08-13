# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:23:38 2020

@author: Teddy
"""
import numpy as np
import networkx as nx
from itertools import product, permutations

#%% Define functions
def draw_graph(G):
    nx.draw_networkx(G, labels={k:'{}:{:.2f}'.format(k,v) for k,v in G.nodes.data('p')}, 
                     node_size=1500, node_color='red')

def collides(x1,x2):
    """ Returns True if x1 collides with x2 """
    return x1[0] < x2[1] and x1[1] > x2[0]
   
def disburse_mass(G, m):
    """ Disburse the probability mass m over the graph G """
    w = m/G.number_of_nodes()
    for i in G:
        Gsub = G.subgraph([x for x in G.nodes if x!=i and x not in G.neighbors(i)])
        
        G.nodes[i]['p'] += w # Add the mass disbursed to this node
        if len(Gsub) > 0:
            disburse_mass(Gsub, w) # Add the mass disbursed to non-neighboring nodes
    return G
 
#%% Setup the problem: Define probabilities and constraints
gap_size = 5
X = [(a,b) for a,b in permutations(range(gap_size+1), 2) if a<b]
p = np.ones(len(X)) * 0.75
c = [(i, i+j+1) for i,x1 in enumerate(X) for j,x2 in enumerate(X[i+1:]) if collides(x1,x2)]



#%% Calculate probability mass for every outcome (disregard constraints)
q = np.array(list(product([0,1],repeat=len(p))))

pp = 1-p
qq = 1-q

mass = np.product(q*p+ qq*pp, axis=1) # The overall mass for each outcome

#%% Disburse mass based on conflicts
# Convert to graph
G = nx.Graph(c)
nx.set_node_attributes(G,0,'p')

for outcome, m in zip(q.astype(bool), mass):
    Gsub = G.subgraph(np.array(G.nodes)[outcome])
    if len(Gsub) > 0:
        disburse_mass(Gsub, m)
    
draw_graph(G)

