#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
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
    
   
    # Once the problem instance is created, an arbitrary number of scenarios are generated for the seed set problem solution
    n_scenarios = 20
    reachability = sam.reachability_generation(
        inst,
        n_scenarios=n_scenarios
    )
    
    #creating the Gurobi solver object
    prb = LargeScaleInfluence()
    #solving the problem with a LP approach
    of_exact, sol_exact, comp_time_exact = prb.solve(
        dict_data,
        reachability,
        n_scenarios,
        verbose = True
    )
    print(of_exact, sol_exact, comp_time_exact)
    
    #creating the Heuristic solver object
    heu1 = FirstHeuristic()
    #solving the problem with the heuristic approach
    of_heu, sol_heu, comp_time = heu1.solve(
        dict_data,
        reachability,
        n_scenarios
    )
    print(of_heu, sol_heu, comp_time)

    #%% COMPARISON:
    # 1) in sample stability #####################################################################
    test = Tester() #instantiating the tester class
    
    n_repetitions = 50
    n_scenarios_in = 20

    of_grblist, of_ex_boxes=test.in_sample_stability(prb, sam, inst, n_scenarios_in, dict_data, n_repetitions) #in sample resolution method for the exact solver
    of_heulist, of_heu_boxes=test.in_sample_stability(heu1, sam, inst, n_scenarios_in, dict_data, n_repetitions) #in sample resolution method for the heuristic
    
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

    bar_plots_gap(
        of_ex_boxes,
        of_heu_boxes,
        labels,
        'Scenarios',
        "GAP %",
        "GAP between heuristic and exact approach",
        "gap_bar_plot_"+dict_data["gnam"]

    )
    # 2) out of sample stability #######################################################################
    
    n_repetitions=50
    n_scenarios_in = 20 #n of scenarios used to train the model
    n_scenarios_out = 10 #n of scenarios used to test the results obtained
    labels=range(1, n_scenarios_in+1)

    E_inf_grblist, E_ex_boxes=test.out_of_sample_stability(prb, sam, inst,  n_scenarios_in,n_scenarios_out, dict_data, n_repetitions) #out of sample stability for exact solver
    E_inf_heulist, E_heu_boxes=test.out_of_sample_stability(heu1, sam, inst,  n_scenarios_in, n_scenarios_out, dict_data, n_repetitions) #out of sample stability for heuristic

    #plot of the out of sample stability for the exact solver
    bar_plots(
            E_ex_boxes, 
            labels,
            'Scenarios',
            "OF",
            "OF value exact vs. number of scenarios",
            "out_of_sample_grb_"+dict_data["gnam"], 1
            )
    #plot of the out of sample stability for the heuristic
    bar_plots(
            E_heu_boxes, 
            labels,
            'Scenarios',
            "OF",
            "OF value heuristic vs. number of scenarios",
            "out_of_sample_heu_"+dict_data["gnam"], 1
            )

    # 3) VSS solution #######################################################################################
    n_scen_in=50
    n_scen_out=200
    n_repetitions=100
    tresh_res=0.05
    VSS_tot, tresh=test.VSS_solve(
        tresh_res,
        prb,
        heu1,
        dict_data,
        sam,
        inst,
        n_scen_in,
        n_scen_out,
        n_repetitions
    )

    labels=np.around(tresh, 2)
    box_plots(
        VSS_tot, 
        labels,
        r'$\rho$',
        "VSS",
        "VSS_rho",
        "vssrho_"+dict_data["gnam"],
        n_repetitions,
        n_scen_in
        )

    
    # printing results of a file
    file_output = open(
        "./results/exp_general_table.csv",
        "w"
    )
    file_output.write("method, of, sol, time\n")
    file_output.write("{}, {}, {}, {}\n".format(
        "heu", of_heu, sol_heu, comp_time
    ))
    file_output.write("{}, {}, {}, {}\n".format(
        "exact", of_exact, sol_exact, comp_time_exact
    ))
    file_output.close()
    
