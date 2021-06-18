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
        #generate N_scenarios_sol for the reachability generation to train the model on
        #each iteration has a different number of scenarios to analyze how the system behaves when increasing the number of scenarios
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
            ans.append(of) #save all the objective function values in order to be able to do a statistics depending on the number of scenarios
            what=np.zeros(len(ans))
            for j in range(len(what)): 
                what[j]=float(ans[j])
            boxes_data.append(what)

        logging.info("In-sample stability considered vectors: ")
        logging.info("Value of the Objective Function: "+str(boxes_data))
        
        return ans, boxes_data
    

       
    def out_of_sample_stability(self, problem, sampler, instance, n_scenarios_sol, n_scenarios_out, dict_data):
        
        boxes_data=[]
        #also for the out of sample stability a scenario dependent analysis. Each run is performed with a increasing number of scenarios for the seed set resolution
        for i in range(1, n_scenarios_sol+1):
            #Part1: solve the problem and find the seed set
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
            

            #Part2: 
            #once having the seed set, generate new scenario to test the seed on
            reachability_out = sampler.reachability_generation(
                instance,
                n_scenarios=n_scenarios_out
            )
            
            boxes_data.append([])
            sols_vec=np.zeros(n_scenarios_out)
            #a influence expansion is performed on each of the n_scenarios_out sets and the OF values is collected
            for j in range(n_scenarios_out):
                sol_out = self.apply_influence_model(
                    instance, sol,
                    n_scenarios_out, reachability_out[j], dict_data
                )
                sols_vec[j]=sol_out
                ans.append(sol_out)
            #for every i-th trial there will be a list of 100 values
            what=np.zeros(len(ans))
            for m in range(len(what)):
                what[m]=float(ans[m])
            boxes_data[i-1].append(what)

        logging.info("Out-of-sample stability considered vectors: ")
        logging.info("Value of the Objective Function: "+str(boxes_data))

        return ans, boxes_data



    def r_bar_evaluation(self, sampler, instance, n_scenarios, dict_data, tresh):
        #here a frequency count is performed with the aim of finding a mean reachability matrix depending on a threshold parameter
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
        #create the reachability matrix inserting the node i in the j-th reachability list if it's frequency is
        #greater than the threshold
        for j in nods:
            R_bar.append([])
            for i in nods:
                if freqs[j][i]>tresh:
                    R_bar[j].append(i)


        logging.info("Generated mean reachability matrix R(i): ")
        logging.info("Matrix: "+str(R_bar))

        return R_bar

        
    def VSS_solve(self, tresh_res,  prb, heu1, dict_data, sam, inst, n_scen, n_scen_out, n_repetitions):
        #the method is used to compare the out of sample stability results with the one obtained computing the solution of the mean reachability matrix
        tresh=np.arange(0,1,tresh_res) #different thresholds level are used
        VSS_rho_box=[]
        gap_tot=np.zeros([len(tresh), n_repetitions])
        for f in range(n_repetitions): #perform the comparison n times to be able in tracking a statistic
            #create a stochastic reachability
            reachability = sam.reachability_generation(
                    inst,
                    n_scenarios=n_scen
                )
            #solve the problem
            _, sol,_ = prb.solve(
                dict_data,
                reachability,
                n_scen
            )
            
            for i in range(len(tresh)): #perform the analysis for all the threshold levels
                VSS_rho_box.append([])
                n_scenarios=1000
                #get the mean reachability matrix with thershold i
                R_bar=self.r_bar_evaluation(
                    sam, 
                    inst, 
                    n_scenarios, 
                    dict_data,
                    tresh[i]
                    )
                #solve the problem on that mean reachability matrix
                _, sol_det,_ = prb.solve_deterministic(
                    dict_data,
                    R_bar,
                    verbose = False
                )

                #generate the out of sample testing scenarios
                reachability_out = sam.reachability_generation(
                    inst,
                    n_scenarios=n_scen_out
                )

                ans=[]
                #test the stochastic result on the out of sample test scenarios
                for j in range(n_scen_out):
                    sol_out = self.apply_influence_model(
                        inst, sol,
                        n_scen_out, reachability_out[j], dict_data
                    )
                    
                    ans.append(sol_out)
                #test the mean seed set obtained from the solution of the problem with R_bar
                sol_out_det = self.apply_influence_model(
                    inst,
                    sol_det,
                    1,
                    R_bar,
                    dict_data
                )
                #compute their difference and track mean value and variance 
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


        logging.info("VSS solution of the algorithm for varying treshold: ")
        logging.info(r'$\rho$'"=: range(0,1,"+str(tresh_res))
        logging.info("Data: "+str(corr_ds))

        return corr_ds, tresh


