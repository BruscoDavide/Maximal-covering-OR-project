# -*- coding: utf-8 -*-
import logging
import numpy as np
import networkx as nx

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

def generate_graph(fname):
    fp=open(fname, 'r')
    Lines=fp.readlines()
    vec=[]

    for line in Lines:
        x=line.split()
        vec.append([int(x[0]), int(x[1])])

    g=nx.DiGraph()

    for i in range(len(vec)):
        from_node=vec[i][0]
        to_node=vec[i][1]
        g.add_edge(from_node, to_node)

    return g
    

class Instance():
    def __init__(self, sim_setting):
        logging.info("starting simulation...")
        self.graph_order = sim_setting['Graph_Order']
        self.K = sim_setting['Seed_card']
        self.graph_seed=seed=sim_setting['Graph_seed_generation']
        
        #self.g=generate_graph(fname)
        self.g=nx.erdos_renyi_graph(sim_setting['Graph_Order'], 0.4, seed=self.graph_seed, directed=True)

        self.g=assign_weights(self.g)
        self.adj_mat=self.g._adj

        logging.info(f"Order of the graph: {self.graph_order}")
        logging.info(f"Maximum seeds to be considered: {self.K}")
        logging.info(f"Adjacency Matrix: {self.adj_mat}")
        logging.info(f"Seed of the graph: {self.graph_seed}")
        logging.info("simulation end")

    def get_data(self):
        logging.info("getting data from instance...")
        return {
            "Order": self.graph_order,
            "K": self.K,
            "Seed": self.graph_seed,
            "Adj_mat": self.adj_mat,
            "Graph" : self.g
        }
