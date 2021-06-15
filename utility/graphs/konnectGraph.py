# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 23:32:12 2021

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



#create graph form konnect

fp = open("out.txt",'r')
konnect_g = nx.DiGraph()
node_list = []

for line in fp:
    l = line.split()
    if l[0] not in node_list:
        konnect_g.add_node(l[0])
    if l[1] not in node_list:
        konnect_g.add_node(l[0])
    konnect_g.add_edge(l[0],l[1])
    
konnect_g = assign_weights(konnect_g)
pos = nx.spring_layout(konnect_g)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(konnect_g, pos, node_size=400)
nx.draw_networkx_edges(konnect_g, pos)
nx.draw_networkx_labels(konnect_g, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    