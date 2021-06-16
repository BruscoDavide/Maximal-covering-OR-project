# -*- coding: utf-8 -*-
import logging
import numpy as np
import networkx as nx
import random
import sys

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

def curated_graph():
    orders = 14
    curated = nx.DiGraph()
    for i in range(orders):
        curated.add_node(i)
        
    main_nodes = [2,4] 
    nodes = np.arange(0,orders,1)
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
    return curated, orders

def random_graph(order, graph_seed):
    g = nx.generators.directed.scale_free_graph(order, 0.01, 0.39,0.6, 3, 4, seed=graph_seed)
    ad = g._adj

    copy = nx.DiGraph()
    for node in g.nodes:
        copy.add_node(node)
        
    for keys in ad:
        ad_row = ad[keys]
        for elem in ad_row:
            copy.add_edge(keys, elem)
        
    ad_copy = copy._adj
            
    copy = assign_weights(copy)

    return copy

def konect_graph(fp):
        konnect_g = nx.DiGraph()
        node_list = []
    
        for line in fp:
            l = line.split()
            if int(l[0])-1 not in node_list:
                konnect_g.add_node(int(l[0])-1)
            if int(l[1])-1 not in node_list:
                konnect_g.add_node(int(l[0])-1)
            konnect_g.add_edge(int(l[0])-1,int(l[1])-1)
            
        
        konnect_g = assign_weights(konnect_g)  
        
        return konnect_g, konnect_g.order() 



class Instance():
    
    
    
    def __init__(self, sim_setting):
        logging.info("starting simulation...")
        self.graph_order = sim_setting['Graph_Order']
        self.K = sim_setting['Seed_card']
        self.graph_seed=sim_setting['Graph_seed_generation']
        self.fname=sim_setting['File_Name_Graph']
        
        try:
            if sim_setting["Graph_type"]=='curated':
                self.g, nodes=curated_graph()
                self.graph_order=nodes
            elif sim_setting["Graph_type"]=='random':
                self.g=random_graph(sim_setting['Graph_Order'], self.graph_seed)
            elif sim_setting["Graph_type"]=='konect':
                self.g, nodes=konect_graph(sim_setting["fp"])
                self.graph_order=nodes
        except:
            print("No graph type exists with specified type")
            sys.exit(1)
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
