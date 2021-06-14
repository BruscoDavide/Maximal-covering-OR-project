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
from utility.plot_results import plot_comparison_hist, box_plots

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
    # n_scenarios_in = 10
    # n_repetitions = 100

    # of_grblist=test.in_sample_stability(prb, sam, inst, n_repetitions, n_scenarios_in, dict_data)

    # print("List of sols gurobi: "+str(of_grblist))

    # of_heulist=test.in_sample_stability(heu1, sam, inst, n_repetitions, n_scenarios_in, dict_data)

    # print("List of sols heuristic: "+str(of_heulist))



    # plot_comparison_hist(
    #         [of_grblist, of_heulist],
    #         ["Exact", "Heuristic"],
    #         ['red', 'blue'],
    #         "E[nodes_influenced]", "occurencies", 0
    #     )

    # #COMPARISON:
    # #out of sample stability


    # n_scenarios_in = 10
    # n_scenarios_out = 100
    # n_repetitions = 10

    # E_inf_grblist=test.out_of_sample_stability(prb, sam, inst, n_repetitions, n_scenarios_in,n_scenarios_out, dict_data)

    # E_inf_heulist=test.out_of_sample_stability(heu1, sam, inst, n_repetitions, n_scenarios_in, n_scenarios_out, dict_data)


    # plot_comparison_hist(
    #     [E_inf_grblist, E_inf_heulist],
    #     ["Exact", "Heuristic"],
    #     ['red', 'blue'],
    #     "E[nodes_influenced]", "occurencies", 1
    # )

    #VSS solution

    #First evaluate Rbar(i)

    # tresh=np.arange(0,1,0.1)
    VSS_rho_box=[]
    tresh=[0.71]
    for i in range(len(tresh)):
        VSS_rho_box.append([])
        VSS_rho_box[i].append(of_exact)
        VSS_rho_box[i].append(of_heu)
        n_scenarios=100

        R_bar=test.r_bar_evaluation(
            sam, 
            inst, 
            n_scenarios, 
            dict_data,
            tresh[i]
            )


        n_scenarios=1

        of_exact_d, sol_exact_d, comp_time_exact_d = prb.solve_deterministic(
            dict_data,
            R_bar,
            verbose = False
        )
        # print(of_exact_d, sol_exact_d, comp_time_exact_d)
        VSS_rho_box[i].append(of_exact_d)

        of_heu_d, sol_heu_d, comp_time_d = heu1.solve_deterministic(
            dict_data,
            R_bar
        )
     
        # print(of_heu_d, sol_heu_d, comp_time_d)
        VSS_rho_box[i].append(of_heu_d)

    box_plots(VSS_rho_box)

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
    
