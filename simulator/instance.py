# -*- coding: utf-8 -*-
import logging
import numpy as np
import networkx as nx
import random
import sys

def assign_weights(g):
    #FUNCTION DESCRIPTION: the method takes as input a directed graph and it assigns for each link a weight. The weights represent the
    #probability that a node has to influence its successors and this number is influenced by the total number of neighbors the node under
    #analysis has. Higher the node degree, higher will be the weight of that edge. To not make the process deterministic, a 20% noise fluctuation
    #is insert to each value.
    maxim=0
    for j in g.nodes: #scanning all the nodes in the graph
        fff=[]
        for i in g.successors(j): #extracting all the successors of the node
            fff.append(i)
            
        weig=len(fff)
        
        for i in g.successors(j):
            weig_arc=weig+np.random.uniform(-0.2*weig,0.2*weig)
            g[j][i]['weight']=weig_arc
            if weig_arc>maxim:
                maxim=weig_arc #save the maximum weight for the normalization procedure at the end
    
    for j in g.nodes: #normalizing the weigths respect the maximum
        for i in g.successors(j):
            g[j][i]['weight']=g[j][i]['weight']/maxim
    return g

#Now it follows 3 functions used for the graph creation:
# 1) the curated graph is used as a initial analysis on the model to check if the mathematical model works.
def curated_graph():
    orders = 14 #only 14 nodes used for simplicity
    curated = nx.DiGraph()
    for i in range(orders):
        curated.add_node(i)
        
    main_nodes = [2,4] #main central nodel, they represent the influencers in the graph
    nodes = np.arange(0,orders,1)
    nodes = list(nodes)

    for i in range(len(main_nodes)):
        nodes.remove(main_nodes[i])
    random.shuffle(nodes)

    curated.add_edge(main_nodes[0], main_nodes[1])  #the two main nodes are conncected one to the other
    curated.add_edge(main_nodes[1], main_nodes[0])

    neigh_per_node = 6 #to each node there are connected 6 neighbors
    for core in main_nodes:
        for i in range(neigh_per_node):
            curated.add_edge(core, nodes[0])
            nodes.remove(nodes[0])
            
    curated = assign_weights(curated)
    return curated, orders

# 2) a scale free graph is realized for intermediate testing.
def random_graph(order, graph_seed):
    #the networkX library was allowing to create a scale free graph, but it was not allowing to modify the weights.
    #After a preliminary analysis where the parameters for the attachment were tuned, then the graph was copied to a DiGraph()
    #to be able to randomly assign the weights
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

#3) The third graph is retrieved from a third pary site. The graph arrives as an adjacence list, so it has to be trasformed in a
#networkX graph instance
def konect_graph(fp):
        konnect_g = nx.DiGraph()
        node_list = []
    
        for line in fp: #read line by line
            l = line.split() #split the line as [edge source, edge destination]
            if int(l[0])-1 not in node_list: #if the node doesn't exist, add it
                konnect_g.add_node(int(l[0])-1)
            if int(l[1])-1 not in node_list:
                konnect_g.add_node(int(l[0])-1)
            konnect_g.add_edge(int(l[0])-1,int(l[1])-1) #create the edge
            
        
        konnect_g = assign_weights(konnect_g)  
        
        return konnect_g, konnect_g.order() 

def erdos_renyi(order):
    edge_prob = 0.8
    ER_g = nx.erdos_renyi_graph(order, edge_prob)
    g_copy = nx.DiGraph()

    for i in range(order):
        g_copy.add_node(i)

    adj = ER_g._adj

    for i in range(len(adj)):
        neighbors = adj[i].keys()
        for neigh in neighbors:
            g_copy.add_edge(i, neigh)
    
    g_copy = assign_weights(g_copy)
    
    return g_copy


def watt_strogatz(order):
    edge_prob = 0.4
    n_neigh = int(order/10)
    WS_g = nx.watts_strogatz_graph(order, n_neigh, edge_prob)      
    g_copy = nx.DiGraph()
    for i in range(order):
        g_copy.add_node(i)

    adj = WS_g._adj

    for i in range(len(adj)):
        neighbors = adj[i].keys()
        for neigh in neighbors:
            g_copy.add_edge(i, neigh)

    g_copy = assign_weights(g_copy)

    return g_copy


def regular_random(order):
    node_degree = 5
    random_reg = nx.random_regular_graph(node_degree, order)
    g_copy = nx.DiGraph()
    for i in range(order):
        g_copy.add_node(i)

    adj = random_reg._adj

    for i in range(len(adj)):
        neighbors = adj[i].keys()
        for neigh in neighbors:
            g_copy.add_edge(i, neigh)

    g_copy = assign_weights(g_copy)

    return g_copy


def barabasi_albert(order):
    stubs = 3 #connection from the new node to the already existing
    BA_g = nx.barabasi_albert_graph(order, stubs)
    g_copy = nx.DiGraph()
    for i in range(order):
        g_copy.add_node(i)

    adj = BA_g._adj

    for i in range(len(adj)):
        neighbors = adj[i].keys()
        for neigh in neighbors:
            g_copy.add_edge(i, neigh)

    g_copy = assign_weights(g_copy)

    return g_copy

def powerlaw_cluster(order):
    stubs = 3 #connection from the new node to the already existing
    prob = 0.8
    powerclust = nx.powerlaw_cluster_graph(order, stubs, prob)
    g_copy = nx.DiGraph()
    for i in range(order):
        g_copy.add_node(i)

    adj = powerclust._adj

    for i in range(len(adj)):
        neighbors = adj[i].keys()
        for neigh in neighbors:
            g_copy.add_edge(i, neigh)

    g_copy = assign_weights(g_copy)

    return g_copy

def random_lobster(order):
    p1 = 0.7
    p2 = 0.4
    rand_lobster = nx.random_lobster(order, p1, p2)
    g_copy = nx.DiGraph()
    for i in range(order):
        g_copy.add_node(i)

    adj = rand_lobster._adj

    for i in range(len(adj)):
        neighbors = adj[i].keys()
        for neigh in neighbors:
            g_copy.add_edge(i, neigh)

    g_copy = assign_weights(g_copy)

    return g_copy





class Instance(): 

    def __init__(self, sim_setting): #create the graph instance depending on the sim_settings file
        logging.info("starting simulation...")
        self.graph_order = sim_setting['Graph_Order']
        self.K = sim_setting['Seed_card']
        self.graph_seed=sim_setting['Graph_seed_generation']
        self.fname=sim_setting['File_Name_Graph']
        self.gname=sim_setting['Graph_type']
        
        try:
            if sim_setting["Graph_type"]=='curated':
                self.g, nodes=curated_graph()
                self.graph_order=nodes
            elif sim_setting["Graph_type"]=='random':
                self.g=random_graph(sim_setting['Graph_Order'], self.graph_seed)
            elif sim_setting["Graph_type"]=='konect':
                self.g, nodes=konect_graph(sim_setting["fp"])
                self.graph_order=nodes
            elif sim_setting["Graph_type"]=='erdos_renyi':
                self.g = erdos_renyi(self.graph_order)
            elif sim_setting["Graph_type"]=='watt_strogatz':
                self.g = watt_strogatz(self.graph_order)
            elif sim_setting["Graph_type"]=='regular_random':
                self.g = regular_random(self.graph_order)
            elif sim_setting["Graph_type"]=='barabasi_albert':
                self.g = barabasi_albert(self.graph_order)
            elif sim_setting["Graph_type"]=='powerlaw_cluster':
                self.g = powerlaw_cluster(self.graph_order)
            elif sim_setting["Graph_type"]=='random_lobster':
                self.g = random_lobster(self.graph_order)

        except: #error handler
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
            "Graph" : self.g,
            "gnam" : self.gname
            
        }
