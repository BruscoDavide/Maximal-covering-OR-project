# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 21:28:28 2021

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








'''
alfa+beta+gamma = 1
alpha = probabilita' di connettere un nuovo nodo ad un nodo gia' esistente scelto in base a quanti nodi ha in ingresso
beta = probabilita' di connettere un nodo gia' esistente. Un nodo e' scelto in base alla in degree e l'altro in base alla out degree
gamma = probailita' di aggiungere un nuovo nodo ad un nodo esistente in base alla out degree distribution
'''
g = nx.generators.directed.scale_free_graph(50, 0.01, 0.39,0.6, 3, 4, seed = 42)
ad = g._adj


pos = nx.spring_layout(g)  # positions for all nodes
# nodes
nx.draw_networkx_nodes(g, pos, node_size=400)
nx.draw_networkx_edges(g, pos)
nx.draw_networkx_labels(g, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()

copy = nx.DiGraph()
for node in g.nodes:
    copy.add_node(node)
    
for keys in ad:
    ad_row = ad[keys]
    for elem in ad_row:
        copy.add_edge(keys, elem)
    
ad_copy = copy._adj
        
copy = assign_weights(copy)
