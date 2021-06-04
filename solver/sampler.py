# -*- coding: utf-8 -*-
import numpy as np
import random


class Sampler:
    def __init__(self):
        pass

    def reachability_generation(self, instance, n_scenarios):
        nod=instance.adj_mat

        nodes=range(instance.graph_order)
        scenarios=range(n_scenarios)

        reach=np.zeros([n_scenarios, instance.graph_order, instance.graph_order], dtype=int)

        for w in scenarios:
            for i in nodes:
                for j in instance.g.predecessors(i): 
                
                    temp = np.around(np.random.uniform(0,1),4)
                    if temp<=nod[j][i]['weight']:
                        reach[w][i][j]=1
        return reach

