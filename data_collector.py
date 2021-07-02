# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 22:17:07 2021

@author: soxst
"""

import os
import json

graph_list = ['erdos_renyi', 'watt_strogatz', 'regular_random', 'barabasi_albert','powerlaw_cluster', 'random_lobster', 'konect']
while graph_list != []:
    graph_type = graph_list.pop(0)
    fp = open("etc//sim_setting.json", 'r')
    settings = json.load(fp)
    fp.close()
    settings["Graph_type"] = graph_type
    if graph_type == 'konect':
        settings["Seed_card"] = 15
    elif graph_type == 'random_lobster':
        settings["Seed_card"] = 10
    else:
        settings["Seed_card"] = 2
    fp = open("etc/sim_setting.json", 'w')
    json.dump(settings,fp)
    fp.close()
    
    os.system("main_in_sample.py")
    
    