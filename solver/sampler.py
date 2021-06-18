# -*- coding: utf-8 -*-
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import logging

def plotter_scenario(R, g, n_scen, n_order):
    
    for w in range(n_scen):
        g_R=nx.DiGraph()
        considered=R[w]
        for i in range(n_order):
            for j in considered[i]:
                g_R.add_edge(j, i, weight=g[j][i]["weight"])

        plt.figure()
        pos = nx.spring_layout(g_R)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(g_R, pos, node_size=400)
        nx.draw_networkx_edges(g_R, pos)

        # # edges
        # nx.draw_networkx_edges(g, pos, edgelist=elarge, width=6)
        # nx.draw_networkx_edges(
        #     g, pos, edgelist=esmall, width=5, alpha=0.5
        # )

        # labels
        nx.draw_networkx_labels(g_R, pos, font_size=20, font_family="sans-serif")

        plt.axis("off")
        plt.show()
  

class Sampler:
    #class used to create the scenarios.
    def __init__(self):
        pass

    def reachability_generation(self, instance, n_scenarios):
        #the reachability matrix is a 3D data structure where every row represent a new scenario
        #each row contains n_nodes lists, each representing the reachability set per node. By reachability list is meant
        #the set of nodes influencing node_j
        nod=instance.adj_mat
        nodes=range(instance.graph_order)
        scenarios=range(n_scenarios)

        reach=np.zeros([n_scenarios, instance.graph_order], dtype=list)

        for w in scenarios:
            for i in nodes:
                reach[w][i]=[]
                for j in instance.g.predecessors(i): #for each node are inspected its predecessors
                    temp = np.around(np.random.uniform(0,1),4) #extract a random uniform probability sample
                    #the sample represent the "resistence" the node is opposing to the influence
                    if temp<=nod[j][i]['weight']: #if the resistence il lower than the influence on the edge, the node is influenced
                        reach[w][i].append(j)


        # plotter_scenario(reach, instance.g, n_scenarios, instance.graph_order)
        logging.info("Reachability matrices generated: "+str(reach))
        return reach

