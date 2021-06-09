# -*- coding: utf-8 -*-
import os
import time
import logging
import json
import numpy as np
import gurobipy as gp
from gurobipy import GRB


class Tester():
    def __init__(self):
        pass

    def compare_sols_lst(
        self, inst, sampler, sols, labels, n_scenarios
    ):

        """
        questo compare io non lo farei cosi', ma prenderei i due histogrammi e comparerei ogni nodo per vedere
        lo scarto delle due barre.

        """
        ans_dict = {}
        reward = sampler.sample_stoch(
            inst,
            n_scenarios=n_scenarios
        )
        for j in range(len(sols)):
            profit_raw_data = self.solve_second_stages(
                inst, sols[j],
                n_scenarios, reward
            )
            ans_dict[labels[j]] = profit_raw_data

        return ans_dict

    #noi non abbiamo nessun second stage solution
    """  def solve_second_stages(
        self, inst, sol, n_scenarios, reward
    ):
        ans = []
        obj_fs = 0
        for i in range(inst.n_items):
            obj_fs += inst.profits[i] * sol[i]
        items = range(inst.n_items)
        for s in range(n_scenarios):
            problem_name = "SecondStagePrb"
            model = gp.Model(problem_name)
            Y = model.addVars(
                inst.n_items,
                lb=0,
                ub=1,
                vtype=GRB.INTEGER,
                name='Y'
            )

            obj_funct = gp.quicksum(reward[i, s] * Y[i] for i in items)

            model.setObjective(obj_funct, GRB.MAXIMIZE)
            
            model.addConstr(
                gp.quicksum(inst.sizes_ss[i] * Y[i] for i in items) <= inst.max_size_ss,
                f"volume_limit_ss"
            )
            for i in items:
                model.addConstr(
                    Y[i] <= sol[i],
                    f"link_X_Y_for_item_{i}"
                )
            model.update()
            model.setParam('OutputFlag', 0)
            model.setParam('LogFile', './logs/gurobi.log')
            model.optimize()
            ans.append(obj_fs + model.getObjective().getValue())

        return ans """

    def in_sample_stability(self, problem, sampler, instance, n_repertions, n_scenarios_sol):
        ################### codice fadda ###################
        """ans = [0] * n_repertions
        for i in range(n_repertions):

        reward = sampler.sample_stoch(
            instance,
            n_scenarios=n_scenarios_sol
        )
        of, sol, comp_time = problem.solve(
            instance,
            reward,
            n_scenarios_sol
        )
        ans[i] = of """
        ####################################################

        """
        nella parte del tester dobbiamo prendere l'istanza del grafo e farci N_reachability matr (che corrispondono a 
        reward 1 e reward 2). Una volta create ste reachability, proviamo ad usare il seed trovato dalla soluzione
        del problema e vedere come si comporta il programma e se da' risultati simili.
        Se le istanze differenti si comportano in maniera piu' o meno uguale, allora  abbia in sample stability
        dubbio: devono essere simili in termini di quanti nodi vengono influenzati, in termini del seed che viene selezionato o dei dei nodi
        che vengono attivati?
        per come l'ho intesa io, per avere stabilita', alla fine si deve avere una distribuzione simile dei nodi influenzati.
            
        """

        '''
        PSEUDOCODE di cio' che serve a noi:
        node_distr_rep = [[]]*n_repetitions
        for i in range(n_repetitions):
            reach = sampler.reachability_genereation(instance, n_scenarios)
            -solve exact model
            -estrarre Z

            =================> tipo qua dovrebbe finire la in sample stab e di base ci salveremmo solo i nodi Z e ne faremmo gli hist

            node_freq = [0]*inst.n_nodes
            for w in range(number_scenarios)
                r = reach[w][:]
                creo grafo di questa reachability
                applico espansione dal set di nodi z
                controllo quali sono attivi e aggiorno le frequenze per ogni nodo

            #qua salvo i risultati di questa run
            node_distr_rep[i] = node_freq

        alla fine di tutto bisognerebbe trovare un modo per paragonare le frequenze di tutte le prove
        come possiamo fare a confrontarle?
        qual e' una metrica accettabile? quanto scarto possiamo accettare?

        NOTA: per quanto riguarda gli histogrammi, piu' sono ripidi e si avvicinano ad una delta, piu' e' stabile

        '''
        

        return ans
    

    """
    poi qua la out of sample stability e' legata al second stage, ma noi nel nostro caso non abbiamo second stage, quindi come si dovrebbe procedere?
    l'unica distinzione che noi possiamo fare tra first e second stage e' definire come first stage quando troviamo Z e second stage quando
    dal seed Z vogliamo espandere l'influenza sul grafo e definiamo cosa succede

    quindi di base = > 
    first stage = trovo le z per tanti problemi e vedo se sono simili
    second stage = trovo tante z e applico il modello di espansione e controllo che anche queste soluzioni siano simili
    
    la prima la si fa in in sample stab, la seconda in out of sample stab
    """
    def out_of_sample_stability(self, problem, sampler, instance, n_repertions, n_scenarios_sol, n_scenarios_out):
        ans = [0] * n_repertions
        for i in range(n_repertions):
            reward= sampler.sample_stoch(
                instance,
                n_scenarios=n_scenarios_sol
            )
            of, sol, comp_time = problem.solve(
                instance,
                reward,
                n_scenarios_sol
            )
            reward_out = sampler.sample_stoch(
                instance,
                n_scenarios=n_scenarios_out
            )
            profits = self.solve_second_stages(
                instance, sol,
                n_scenarios_out, reward_out,
                "profit"
            )
            ans[i]=np.mean(profits)
            
        return ans
