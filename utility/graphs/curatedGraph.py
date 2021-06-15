# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 22:33:46 2021

@author: soxst
"""

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt


def assign_weights(g):
    maxim=0
    for j in g.nodes:
        fff=[]
        for i in g.successors(j):
            fff.append(i)
            
        weig=len(fff)
        
        for i in g.successors(j):
            weig_arc=weig+np.random.uniform(-0.2*weig,0.2*weig)
            g[j][i]['weight']=weig_arc
            if weig_arc>maxim:
                maxim=weig_arc
    
    for j in g.nodes:
        for i in g.successors(j):
            g[j][i]['weight']=g[j][i]['weight']/maxim
    return g



nodes = 14
curated = nx.DiGraph()
for i in range(nodes):
    curated.add_node(i)
    
main_nodes = [2,4] 
nodes = np.arange(0,nodes,1)
nodes = list(nodes)

for i in range(len(main_nodes)):
    nodes.remove(main_nodes[i])
random.shuffle(nodes)

curated.add_edge(main_nodes[0], main_nodes[1])
curated.add_edge(main_nodes[1], main_nodes[0])

neigh_per_node = 6
for core in main_nodes:
    for i in range(neigh_per_node):
        curated.add_edge(core, nodes[0])
        nodes.remove(nodes[0])
        
curated = assign_weights(curated)
pos = nx.spring_layout(curated)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(curated, pos, node_size=400)
nx.draw_networkx_edges(curated, pos)
nx.draw_networkx_labels(curated, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()

        