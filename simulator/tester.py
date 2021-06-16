# -*- coding: utf-8 -*-
import os
import time
import logging
import json
from networkx.classes.function import nodes
import numpy as np
import gurobipy as gp
from gurobipy import GRB

def compute_succ(g, R, z_j):
    succ_computed=[]
    for i in range(len(R)):
        for j in R[i]:
            if j==z_j:
                succ_computed.append(i)
    return succ_computed


class Tester():
    def __init__(self):
        pass

    

    

    #noi non abbiamo nessun second stage solution
    def apply_influence_model(
        self, inst, sol, n_scenarios, reachability, dict_data
    ):

        
        activated_set=[]
        activating_set=[]


        for i in range(len(sol)):
            ml=sol[i]
            if ml==1:
                activating_set.append(i)            
                activated_set.append(i)

        while activating_set!=[]:
            j=activating_set.pop()
            fiter=compute_succ(dict_data["Graph"], reachability, j)
            for f in fiter:
                if f not in activated_set:
                    temp = np.around(np.random.uniform(0,1),4)
                    if temp<=dict_data["Graph"][j][f]['weight']:

                        activated_set.append(f)
                            
        return len(activated_set)
        

    def in_sample_stability(self, problem, sampler, instance, n_scenarios_sol, dict_data):
        ans = []
        boxes_data=[]
        #qua repetitions non si usa piu', si fa andare il programma per n_scnarios_sol per vedere
        #la convergenza in base agli scenari
        for i in range(1,n_scenarios_sol+1):
            
            reachability = sampler.reachability_generation(
                instance,
                n_scenarios=i
            )
            of, sol, comp_time = problem.solve(
                dict_data,
                reachability,
                i
            )
            ans.append(of)
            what=np.zeros(len(ans))
            for j in range(len(what)):
                what[j]=float(ans[j])
            boxes_data.append(what)

            
        # ans=boxes_data[n_repetitions-1]


        return ans, boxes_data
    

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
        
    """
    poi qua la out of sample stability e' legata al second stage, ma noi nel nostro caso non abbiamo second stage, quindi come si dovrebbe procedere?
    l'unica distinzione che noi possiamo fare tra first e second stage e' definire come first stage quando troviamo Z e second stage quando
    dal seed Z vogliamo espandere l'influenza sul grafo e definiamo cosa succede

    quindi di base = > 
    first stage = trovo le z per tanti problemi e vedo se sono simili
    second stage = trovo tante z e applico il modello di espansione e controllo che anche queste soluzioni siano simili
    
    la prima la si fa in in sample stab, la seconda in out of sample stab
    """
    def out_of_sample_stability(self, problem, sampler, instance, n_scenarios_sol, n_scenarios_out, dict_data):
        
        boxes_data=[]
        for i in range(1, n_scenarios_sol+1):
            ans = []
            reachability = sampler.reachability_generation(
                instance,
                n_scenarios=i
            )
            of, sol, comp_time = problem.solve(
                dict_data,
                reachability,
                i
            )
            

            #now out of check
            
            reachability_out = sampler.reachability_generation(
                instance,
                n_scenarios=n_scenarios_out
            )
            
            boxes_data.append([])
            sols_vec=np.zeros(n_scenarios_out)
            for j in range(n_scenarios_out):
                sol_out = self.apply_influence_model(
                    instance, sol,
                    n_scenarios_out, reachability_out[j], dict_data
                )
                sols_vec[j]=sol_out
                ans.append(sol_out)
            what=np.zeros(len(ans))
            for m in range(len(what)):
                what[m]=float(ans[m])
            boxes_data[i-1].append(what)

        return ans, boxes_data



    def r_bar_evaluation(self, sampler, instance, n_scenarios, dict_data, tresh):
        
        reachability = sampler.reachability_generation(
            instance,
            n_scenarios
        )

        nods=range(dict_data["Order"])
        freqs=np.zeros([dict_data["Order"], dict_data["Order"]])
        #compute the relative frequencies of each reach node
        for w in range(n_scenarios):
            reach=reachability[w]
            for j in nods:
                for i in reach[j]:
                    freqs[j][i]+=1
            
        freqs=freqs/n_scenarios
        
        R_bar=[]
        for j in nods:
            R_bar.append([])
            for i in nods:
                if freqs[j][i]>tresh:
                    R_bar[j].append(i)


        return R_bar

        
    def VSS_solve(self, tresh_res,  prb, heu1, dict_data, sam, inst, n_scen, n_scen_out, n_repetitions):
        tresh=np.arange(0,1,tresh_res)
        VSS_rho_box=[]
        gap_tot=np.zeros([len(tresh), n_repetitions])
        for f in range(n_repetitions):
            reachability = sam.reachability_generation(
                    inst,
                    n_scenarios=n_scen
                )
            _, sol,_ = prb.solve(
                dict_data,
                reachability,
                n_scen
            )
            
            for i in range(len(tresh)):
                VSS_rho_box.append([])
                n_scenarios=1000

                R_bar=self.r_bar_evaluation(
                    sam, 
                    inst, 
                    n_scenarios, 
                    dict_data,
                    tresh[i]
                    )

                _, sol_det,_ = prb.solve_deterministic(
                    dict_data,
                    R_bar,
                    verbose = False
                )

                reachability_out = sam.reachability_generation(
                    inst,
                    n_scenarios=n_scen_out
                )

                ans=[]
                for j in range(n_scen_out):
                    sol_out = self.apply_influence_model(
                        inst, sol,
                        n_scen_out, reachability_out[j], dict_data
                    )
                    
                    ans.append(sol_out)

                sol_out_det = self.apply_influence_model(
                    inst,
                    sol_det,
                    1,
                    R_bar,
                    dict_data
                )

                meanans_perc=np.mean(ans)/dict_data["Order"]
                sol_det_perc=sol_out_det/dict_data["Order"]

                gap_step=abs(meanans_perc-sol_det_perc)
                gap_tot[i][f]=gap_step


            # print(of_exact_d, sol_exact_d, comp_time_exact_d)
            # VSS_rho_box[i].append(of_exact_d)


            # of_heu_d, sol_heu_d, comp_time_d = heu1.solve_deterministic(
            #     dict_data,
            #     R_bar
            # )
        
            # print(of_heu_d, sol_heu_d, comp_time_d)
            
            
        # varbs=[]
        # for i in range(len(VSS_rho_box)):
        #     varbs.append(np.var(VSS_rho_box[i]))
            
        # min_var=np.argmin(varbs)
        
        # best_VSS=VSS_rho_box[min_var][2:3]
        
        # best_VSS=np.mean(best_VSS)
        
        # best_tresh=tresh[min_var]
        corr_ds=[]
        for i in range(len(tresh)):
            corr_ds.append([])
            for j in range(n_repetitions):
                corr_ds[i].append(gap_tot[i][j])


        return corr_ds, tresh


