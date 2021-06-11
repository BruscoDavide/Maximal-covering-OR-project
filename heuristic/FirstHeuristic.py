# -*- coding: utf-8 -*-
import time
import math
import logging
import numpy as np

def compute_succ(g, R, z_j):
    succ_computed=[]
    for i in range(len(R)):
        for j in R[i]:
            if j==z_j:
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
        
        start = time.time()
        
        scenarios = range(n_scenarios)
        nodes = range(dict_data['Order'])

        zi=[]

        for w in scenarios:
            reach_scen = reachability[w]

            freqs = np.zeros([dict_data['Order']])

            for i in nodes:
                for j in range(len(reach_scen[i])):
                    freqs[reach_scen[i][j]]+=1

            idx=list(np.argsort(freqs))
            idx.reverse()
            zi.append(idx[0:dict_data['K']])
            
        of=0
        p=1/n_scenarios
        for w in scenarios:
    
            activated_set=[]
            activating_set=[]


            for ml in zi[w]:
                activating_set.append(ml)            
                activated_set.append(ml)

            while activating_set!=[]:
                j=activating_set.pop()
                fiter=compute_succ(dict_data["Graph"], reachability[w], j)
                for f in fiter:
                    if f not in activated_set:
                        # temp = np.around(np.random.uniform(0,1),4)
                        # if temp<=dict_data["Graph"][j][f]['weight']:

                        activated_set.append(f)
                                
            of+=len(activated_set)*p

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
