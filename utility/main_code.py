# -*- coding: utf-8 -*-
"""
Created on Fri May 21 13:43:54 2021

@author: ilros
"""
#%% imports and methods
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

#da mettere nel framework

def maxk(array):
    indexes=list(np.argsort(array))
    indexes.reverse()
    
    return indexes


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

#%% start of main

N=5

K=N//100
if K==0:
    K=1

#%% graph generation
# g=nx.DiGraph()
g=nx.erdos_renyi_graph(N, 0.4, seed=42, directed=True)
#stochastic block models
# g=nx.generators.random_graphs.barabasi_albert_graph(10, 2)


#%% weights assignment

g=assign_weights(g)

#%% scenarios creation
nod=g._adj

S=100
Rsi=[]

for keys in nod:
    for i in range(1, S+1):
        line=[keys]
        
        for j in g.predecessors(keys):
            temp = random.randint(1,10000)/10000
            if temp<=nod[j][keys]['weight']:
                line.append(j)
            
        Rsi.append(line)
            
#conviene farlo a matrice        

#%% exact solver needed        

#%% find seeds |zj|<k
#search for the most used node
freqs=np.zeros(N,)


for i in range(0,len(Rsi)):
    for j in Rsi[i]:
        freqs[j]+=1

freqs=freqs-S

poss_seeds=maxk(freqs)

# print(poss_seeds[0:(K)])

seedd=poss_seeds[0:K]
print(seedd)
#%% find expected value of influenced nodes


# find maximum time of simulation
maxim_path=0
for sacks in seedd:
    for keys in nod:
        if keys!=sacks:
            sd=nx.shortest_path(g, sacks, keys)
            if maxim_path<=len(sd):
                maxim_path=len(sd)


E_n=[]
it=np.arange(0,1*N,0.01*N)
for generic_treshold in it:
    
    i=0
    activated_set=[]
    activating_set=[]
    

    for sacks in seedd:
        activating_set.append(sacks)
        activated_set.append(sacks)
        
        
        while i<maxim_path:
            
            while activating_set!=[]:
                j=activating_set.pop()
                for f in g.successors(j):
                    if f not in activated_set:
                        #influencing policy
                        summ=0
                        for m in g.predecessors(f):
                            summ=summ+g[m][f]['weight']
                            
                        if summ>=generic_treshold:
                            activated_set.append(f)
                            activating_set.append(f)
                        #end influencing policy
            
            i=i+1
        
    E_n.append(len(activated_set))


plt.figure()
plt.plot(it, E_n)
plt.ylabel("E[N]")
plt.xlabel("Treshold")
plt.title("Expected number of people influenced with varying treshold")
plt.grid()
plt.show()




#%% Plot graph
# elarge = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] > 0.5]
# esmall = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] <= 0.5]

pos = nx.spring_layout(g)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(g, pos, node_size=400)
nx.draw_networkx_edges(g, pos)

# # edges
# nx.draw_networkx_edges(g, pos, edgelist=elarge, width=6)
# nx.draw_networkx_edges(
#     g, pos, edgelist=esmall, width=5, alpha=0.5
# )

# labels
nx.draw_networkx_labels(g, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()

