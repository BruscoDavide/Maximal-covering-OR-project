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
from utility.plot_results import plot_comparison_hist, box_plots, bar_plots

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

    fp = open("./etc/sim_setting.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    sam = Sampler()


    if sim_setting["Graph_type"]=='konect':
        sim_setting["fp"] =open("./dataset/librec-filmtrust-trust/out.txt",'r')
    inst = Instance(sim_setting)
    dict_data = inst.get_data()
   # print(dict_data)
    
   
    # Reward generation
    n_scenarios = 10
    reachability = sam.reachability_generation(
        inst,
        n_scenarios=n_scenarios
    )

    prb = LargeScaleInfluence()
    of_exact, sol_exact, comp_time_exact = prb.solve(
        dict_data,
        reachability,
        n_scenarios,
        verbose = True
    )
    print(of_exact, sol_exact, comp_time_exact)
    

    heu1 = FirstHeuristic()

    of_heu, sol_heu, comp_time = heu1.solve(
        dict_data,
        reachability,
        n_scenarios
    )

    print(of_heu, sol_heu, comp_time)

        

    


    # COMPARISON:
    # in sample stability
    test = Tester()
    



    n_scenarios_in = 30

    of_grblist, of_ex_boxes=test.in_sample_stability(prb, sam, inst, n_scenarios_in, dict_data)

    of_heulist, of_heu_boxes=test.in_sample_stability(heu1, sam, inst, n_scenarios_in, dict_data)
    
    labels=range(1,n_scenarios_in+1)

    bar_plots(
            of_ex_boxes, 
            labels,
            'Scenarios',
            "OF",
            "OF value exact vs. number of scenarios",
            "in_sample_grb", 0
            )

    bar_plots(
            of_heu_boxes, 
            labels,
            'scenarios',
            "OF",
            "OF value heuristic vs. number of scenarios",
            "in_sample_heu", 0
            )



    # plot_comparison_hist(
    #         [of_grblist, of_heulist],
    #         ["Exact", "Heuristic"],
    #         ['red', 'blue'],
    #         "E[nodes_influenced]", "occurencies", 0
    #     )

    # #COMPARISON:
    # #out of sample stability


    n_scenarios_in = 30
    n_scenarios_out = 100
    labels=range(1, n_scenarios_in+1)
    E_inf_grblist, E_ex_boxes=test.out_of_sample_stability(prb, sam, inst,  n_scenarios_in,n_scenarios_out, dict_data)

    E_inf_heulist, E_heu_boxes=test.out_of_sample_stability(heu1, sam, inst,  n_scenarios_in, n_scenarios_out, dict_data)




    bar_plots(
            E_ex_boxes, 
            labels,
            'Scenarios',
            "OF",
            "OF value exact vs. number of scenarios",
            "out_of_sample_grb", 1
            )

    bar_plots(
            E_heu_boxes, 
            labels,
            'Scenarios',
            "OF",
            "OF value heuristic vs. number of scenarios",
            "out_of_sample_heu", 1
            )


    # plot_comparison_hist(
    #     [E_inf_grblist, E_inf_heulist],
    #     ["Exact", "Heuristic"],
    #     ['red', 'blue'],
    #     "E[nodes_influenced]", "occurencies", 1
    # )

#VSS solution
    n_scen_in=20
    n_scen_out=100
    n_repetitions=10
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
        "vssrho",
        n_repetitions,
        n_scen_in
        )

    '''
    tipo qua definiamo il numero di prove che vogliamo fare.
    ci facciamo ventordici reachability matrices, una per ogni prova che vogliamo provare a fare

    Per aggiungere un po' di spicy, possiamo definire un seed all'interno di sampler cosi' ogni volta che 
    creiamo una reachability matrix, ci viene un po' diversa e abbiamo piu' stocasticita'
    '''

    '''
    poi con quella reachability ed il set Z (sol_exact), facciamo la prova ed espandiamo l'influenza.
    Cosa importante in questo caso, non facciamo piu' la media su tutti i scenari, ma si prende ogni scenario
    in parte, si fa la sua espansione di influenza, ci si salva il numero di nodi attivati in una lista 
    e poi si plotta alla fine l'istogramma
    '''

    """
    per ogni prova ci salviamo i risultati, immagino qualcosa come il numero di nodi attivati e ne tracciamo un 
    istogramma, poi le paragoniamo.
    Si spera le distribuzioni vengano simili
    la cosa che mi crea qualche dubbio e' che questo ragionamento e' molto simile a cio' che si fa per la sample stability e non capisco bene la differenza
    tra i due approcci
    


    in sample: compara objective function di entrambe le soluzioni

    out of sample: compariamo usando un campione molto più grande
    usare numero di scenari molto più grandi rispetto a in sample
    genero degli scenari per gurobi
    genero altri scenari per l'euristica
    nell'out of sample prendo la soluzione dei seed, e uso quelli per vedere quanti ne sono influenzati
    
    
    per il valore atteso (per ogni variabile aleatoria mettiamo il suo valore atteso)
    determinare il valore atteso dei nodi che influenzano
    """


    
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
    
