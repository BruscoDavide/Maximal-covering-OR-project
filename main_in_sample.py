#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import time
import logging
import numpy as np
from simulator.instance import Instance
from simulator.tester import Tester
from solver.LargeScaleInfluence import LargeScaleInfluence
from heuristic.FirstHeuristic import FirstHeuristic
from solver.sampler import Sampler
from utility.plot_results import plot_comparison_hist, box_plots, bar_plots, bar_plots_gap

import matplotlib.pyplot as plt


# np.random.seed(0)

if __name__ == '__main__':
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )

    fp = open("./etc/sim_setting.json", 'r') #opening the setting file
    sim_setting = json.load(fp)
    fp.close()

    sam = Sampler()

    #if the program has to use the graph retrieved from konect.org, then it has to open the adjacence matrix file to
    #transform it in a usable graph
    if sim_setting["Graph_type"]=='konect': 
        sim_setting["fp"] =open("./dataset/librec-filmtrust-trust/out.txt",'r')
    inst = Instance(sim_setting) #create the graph instance
    dict_data = inst.get_data()
    
    prb = LargeScaleInfluence()
    heu1 = FirstHeuristic()
    #%% COMPARISON:
    # 1) in sample stability #####################################################################
    test = Tester() #instantiating the tester class
    
    n_repetitions = 4#30
    n_scenarios_in = 10#100
    time_filename = "etc/time_data_"+sim_setting["Graph_type"]+".json"
    of_filename = "etc/of_data_"+sim_setting["Graph_type"]+".json"
    of_grblist, of_ex_boxes, timings_lp, of_lp = test.in_sample_stability(prb, sam, inst, n_scenarios_in, dict_data, n_repetitions) #in sample resolution method for the exact solver
    #copy the timings
    fp = open(time_filename, 'r')
    time_dict = json.load(fp)
    fp.close()
    time_dict["LP_timing"] = timings_lp
    fp = open(time_filename, 'w')
    json.dump(time_dict, fp)
    fp.close()

    #copy the of values
    fp = open(of_filename, 'r')
    of_dict = json.load(fp)
    fp.close()
    of_dict["LP_of"] = of_lp
    fp = open(of_filename, 'w')
    json.dump(of_dict, fp)
    fp.close()

    of_heulist, of_heu_boxes, timings_heu, of_heu = test.in_sample_stability(heu1, sam, inst, n_scenarios_in, dict_data, n_repetitions) #in sample resolution method for the heuristic
    #copy the timings
    fp = open(time_filename, 'r')
    time_dict = json.load(fp)
    fp.close()
    time_dict["heu_timing"] = timings_lp
    fp = open(time_filename, 'w')
    json.dump(time_dict, fp)
    fp.close()

    #copy the of values
    fp = open(of_filename, 'r')
    of_dict = json.load(fp)
    fp.close()
    of_dict["heu_of"] = of_heu
    fp = open(of_filename, 'w')
    json.dump(of_dict, fp)
    fp.close()


    
    labels=range(1,n_scenarios_in+1)

    #plot the in sample stability results for the exact solution
    bar_plots(
            of_ex_boxes, 
            labels,
            'Scenarios',
            "OF",
            "OF value exact vs. number of scenarios",
            "in_sample_grb_"+dict_data["gnam"], 0
            )
    #plot the in sample stability results for the heuristic solution
    bar_plots(
            of_heu_boxes, 
            labels,
            'scenarios',
            "OF",
            "OF value heuristic vs. number of scenarios",
            "in_sample_heu_"+dict_data["gnam"], 0
            )

    """  bar_plots_gap(
        of_ex_boxes,
        of_heu_boxes,
        labels,
        'Scenarios',
        "GAP %",
        "GAP between heuristic and exact approach",
        "gap_bar_plot_"+dict_data["gnam"]

    ) """
