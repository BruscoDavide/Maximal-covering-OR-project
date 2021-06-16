# -*- coding: utf-8 -*-
import time
import math
import logging
import numpy as np


################
import collections
################

def compute_succ(g, R, z_j):
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
        #start_prova = time.time()
        for w in scenarios:
            reach_scen = reachability[w]
            tmp = []
            tmp2 = []
            for i in reach_scen:
                tmp += i
            
            counter=collections.Counter(tmp)
            common = counter.most_common(dict_data['K'])
            for k in common:
                tmp2.append(k[0])
                zi.append(tmp2)

        #end_prova = time.time()
        #time_prova = end_prova - start_prova
                
        ##########################################

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

        """ freqs = np.zeros([dict_data['Order']])
        for i in zi:
            for j in i:
                freqs[j]+=1
                
        idx=list(np.argsort(freqs))
        idx.reverse()
        
        for i in idx[0:dict_data['K']]:
            sol_z[i]=1 """

        ###############################
        asd = []
        sol_z = []
        for i in zi:
            asd+=i
        freqs = collections.Counter(asd)
        zs = freqs.most_common(dict_data['K'])
        for k in zs:
            sol_z.append(k[0])

        ###############################


        end = time.time()

        comp_time = end - start
        
        
        
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
