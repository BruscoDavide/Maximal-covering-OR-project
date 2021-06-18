# -*- coding: utf-8 -*-
import time
import math
import logging
import numpy as np

################
import collections
################

def compute_succ(g, R, z_j): #inspect the reachability matrix for that scenario.
    #since in the scenario w not all the nodes are activated, only the active nodes have to be take in account, so
    #the successors are selected only among the "alive" edge
    succ_computed=[]
    for i in range(len(R)):
        #for j in R[i]:
        #    if j==z_j:
        if z_j in R[i]:
            succ_computed.append(i)
    return succ_computed



class FirstHeuristic():
    def __init__(self):
        pass

    def solve(
        self, dict_data, reachability, n_scenarios,
    ):
        sol_z = [0] * dict_data['Order']
        of = -1

        scenarios = range(n_scenarios)
        nodes = range(dict_data['Order'])

        zi=[]
        
        start = time.time()
        #the following code was the V1 where a O(N^3) approach was used. For low order graphs it was working properly and it was returning 
        #execution times much lower with respect to the Gurobi solver, but for higher order graphs it was slowing down.
        """ for w in scenarios:  
            reach_scen = reachability[w]

            freqs = np.zeros([dict_data['Order']])

            for i in nodes:
                for j in range(len(reach_scen[i])):
                    freqs[reach_scen[i][j]]+=1

            idx=list(np.argsort(freqs))
            idx.reverse()
            zi.append(idx[0:dict_data['K']])

        end = time.time()

        ufficial = end-start """
            
        ##########################################

        #Using the Collection Python library which has a searching algorithm O(N*log(N)), the searching process increased the perfomances
        #allowing a fast resolution also for high order graphs.
        for w in scenarios:
            reach_scen = reachability[w] #extract the row of the reachability
            tmp = []
            tmp2 = []
            for i in reach_scen: #concatenate the lists
                tmp += i
            
            counter=collections.Counter(tmp) #perform the node frequency count
            common = counter.most_common(dict_data['K']) #extract the K most common nodes, with K defined by sim_settings.json
            for k in common: #append the most common nodes per scenario
                tmp2.append(k[0]) #append only the label of the node, not the number of repetitions
                zi.append(tmp2)
        ##########################################

        #objective function computation:
        of=0
        p=1/n_scenarios
        for w in scenarios:
    
            activated_set=[]
            activating_set=[]


            for ml in zi[w]: #the seed set are the activating nodes, while the activated list keeps track of the nodes influenced by the activating nodes
                activating_set.append(ml)            
                activated_set.append(ml)

            while activating_set!=[]: #extract node by node
                j=activating_set.pop()
                fiter=compute_succ(dict_data["Graph"], reachability[w], j) #extract the successors of those central nodes
                for f in fiter:
                    if f not in activated_set:
                        # temp = np.around(np.random.uniform(0,1),4)
                        # if temp<=dict_data["Graph"][j][f]['weight']:

                        activated_set.append(f)
                                
            of+=len(activated_set)*p

        #seed search V1: again a high computational complexity search was performed which was slowing down the program
        """ freqs = np.zeros([dict_data['Order']])
        for i in zi:
            for j in i:
                freqs[j]+=1
                
        idx=list(np.argsort(freqs))
        idx.reverse()
        
        for i in idx[0:dict_data['K']]:
            sol_z[i]=1 """

        ###############################
        #using the Collections counter, all the seed sets of the scenarios are explored and the K most present are taken as final seed set.
        asd = []
        sol_z_idx = []
        for i in zi:
            asd+=i
        freqs = collections.Counter(asd)
        zs = freqs.most_common(dict_data['K'])
        for k in zs:
            sol_z_idx.append(k[0])

        ###############################


        end = time.time()

        comp_time = end - start

        sol_z = np.zeros([dict_data['Order']])
        sol_z[sol_z_idx] = 1
        
        
        
        return round(of,4), sol_z, comp_time


    def solve_deterministic(
        self, dict_data, reachability
    ):
        sol_z = [0] * dict_data['Order']
        of = -1
        
        start = time.time()
        
        nodes = range(dict_data['Order'])

        zi=[]

        reach_scen = reachability

        freqs = np.zeros([dict_data['Order']])

        #since there is only one scenario to be explored, the Collection library wasn't used
        for i in nodes:
            for j in range(len(reach_scen[i])):
                freqs[reach_scen[i][j]]+=1

        idx=list(np.argsort(freqs))
        idx.reverse()
        zi.append(idx[0:dict_data['K']])
            
        of=0
        p=1

    
        activated_set=[]
        activating_set=[]


        for ml in zi[0]:
            activating_set.append(ml)            
            activated_set.append(ml)

        while activating_set!=[]:
            j=activating_set.pop()
            fiter=compute_succ(dict_data["Graph"], reachability, j)
            for f in fiter:
                if f not in activated_set:
                    # temp = np.around(np.random.uniform(0,1),4)
                    # if temp<=dict_data["Graph"][j][f]['weight']:

                    activated_set.append(f)
                            
        of=len(activated_set)*p

        freqs = np.zeros([dict_data['Order']])
        for i in zi:
            for j in i:
                freqs[j]+=1
                
        idx=list(np.argsort(freqs))
        idx.reverse()
        
        for i in idx[0:dict_data['K']]:
            sol_z[i]=1

        end = time.time()

        comp_time = end - start
        
        
        
        return round(of,4), sol_z, comp_time
