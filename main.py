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
from utility.plot_results import plot_comparison_hist

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

    # mean_reward = sam.sample_ev(
    #     inst,
    #     n_scenarios=n_scenarios
    # )
    # print(mean_reward)

    # prb = SimpleKnapsack()
    # of_exact, sol_exact, comp_time_exact = prb.solve(
    #     dict_data,
    #     reward,
    #     n_scenarios,
    #     verbose=True
    # )
    # print(of_exact, sol_exact, comp_time_exact)

    # COMPARISON:
    # test = Tester()
    # n_scenarios = 1000
    '''
    tipo qua definiamo il numero di prove che vogliamo fare.
    ci facciamo ventordici reachability matrices, una per ogni prova che vogliamo provare a fare

    Per aggiungere un po' di spicy, possiamo definire un seed all'interno di sampler cosi' ogni volta che 
    creiamo una reachability matrix, ci viene un po' diversa e abbiamo piu' stocasticita'
    '''
    # reward_1 = sam.sample_stoch( 
    #     inst,
    #     n_scenarios=n_scenarios
    # )
    '''
    poi con quella reachability ed il set Z (sol_exact), facciamo la prova ed espandiamo l'influenza.
    Cosa importante in questo caso, non facciamo piu' la media su tutti i scenari, ma si prende ogni scenario
    in parte, si fa la sua espansione di influenza, ci si salva il numero di nodi attivati in una lista 
    e poi si plotta alla fine l'istogramma
    '''
    # ris1 = test.solve_second_stages(
    #     inst,
    #     sol_exact,
    #     n_scenarios,
    #     reward_1
    # )
    # reward_2 = sam.sample_stoch(
    #     inst,
    #     n_scenarios=n_scenarios
    # )
    # ris2 = test.solve_second_stages(
    #     inst,
    #     sol_exact,
    #     n_scenarios,
    #     reward_2
    # )
    """
    per ogni prova ci salviamo i risultati, immagino qualcosa come il numero di nodi attivati e ne tracciamo un 
    istogramma, poi le paragoniamo.
    Si spera le distribuzioni vengano simili
    la cosa che mi crea qualche dubbio e' che questo ragionamento e' molto simile a cio' che si fa per la sample stability e non capisco bene la differenza
    tra i due approcci
    """
    # plot_comparison_hist(
    #     [ris1, ris2],
    #     ["run1", "run2"],
    #     ['red', 'blue'],
    #     "profit", "occurencies"
    # )

    '''
    heu = SimpleHeu(2)
    of_heu, sol_heu, comp_time_heu = heu.solve(
        dict_data
    )
    print(of_heu, sol_heu, comp_time_heu)

    # printing results of a file
    file_output = open(
        "./results/exp_general_table.csv",
        "w"
    )
    file_output.write("method, of, sol, time\n")
    file_output.write("{}, {}, {}, {}\n".format(
        "heu", of_heu, sol_heu, comp_time_heu
    ))
    file_output.write("{}, {}, {}, {}\n".format(
        "exact", of_exact, sol_exact, comp_time_exact
    ))
    file_output.close()
    '''
