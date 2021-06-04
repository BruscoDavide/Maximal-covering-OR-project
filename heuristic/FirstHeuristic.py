# -*- coding: utf-8 -*-
import time
import math
import logging
import numpy as np

class FirstHeuristic():
    def __init__(self):
        pass

    def solve(
        self, dict_data, reachability, n_scenarios,
    ):
        sol_x = [0] * dict_data['Order']
        of = -1
        
        start = time.time()
        
        scenarios = range(n_scenarios)
        nodes = range(dict_data['Order'])

        zi=[]

        for w in scenarios:
            reach_scen = reachability[w]

            freqs = np.zeros([dict_data['Order']])

            for i in nodes:
                for j in nodes:
                    freqs[i]+=reach_scen[j][i]

            idx=list(np.argsort(freqs))
            idx.reverse()
            zi.append(idx[0:dict_data['K']])

        print(zi)
            
        su=0
        for w in scenarios:
    
            activated_set=[]
            activating_set=[]


            for i in nodes:
                for ml in zi[w]:
                    activating_set.append(ml)            
                    activated_set.append(zi[w])

                while activating_set!=[]:
                    j=activating_set.pop()
                    for f in dict_data["Graph"].successors(j):
                        if f not in activated_set:
                            temp = np.around(np.random.uniform(0,1),4)
                            if temp<=dict_data["Graph"][j][f]['weight']:

                                activated_set.append(f)
                                
            su+=len(activated_set)


            '''
            summ=0
            for m in dict_data["Graph"].predecessors(f):
                summ=summ+dict_data["Graph"][m][f]['weight']

            if summ >= generic_treshold:
                activated_set.append(f)
                activating_set.append(f)
            '''


        of=su/n_scenarios

        end = time.time()

        comp_time = end - start
        
        return of, sol_x, comp_time
