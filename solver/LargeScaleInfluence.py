# -*- coding: utf-8 -*-
import time
import logging
import gurobipy as gp
from gurobipy import GRB


class LargeScaleInfluence():
    def __init__(self):
        pass

    def solve(
        self, dict_data, reachability, n_scenarios, time_limit=None,
        gap=None, verbose=False
    ):
        nodes = range(dict_data['Order'])
        scenarios = range(n_scenarios)

        problem_name = "LargeSI"
        logging.info("{}".format(problem_name))
        # logging.info(f"{problem_name}")

        model = gp.Model(problem_name)
        X = model.addVars(
            dict_data['Order'], n_scenarios,
            lb=0,
            ub=1,
            vtype=GRB.INTEGER,
            name='X'
        )

        Z = model.addVars(
            dict_data['Order'],
            lb=0,
            ub=1,
            vtype=GRB.INTEGER,
            name='Z'
        )



        p=1/n_scenarios

        obj_funct = 0
        for w in scenarios:
            obj_funct += p * gp.quicksum(X[i,w] for i in nodes)
            
        model.setObjective(obj_funct, GRB.MAXIMIZE)

        model.addConstr(
            gp.quicksum( Z[i] for i in nodes) <= dict_data['K'],
            f"Constraint on starting seed"
        )


        for w in scenarios:
            for i in nodes:
                model.addConstr(
                            X[i,w] <= gp.quicksum(Z[j] for j in reachability[w][i])
                )

        model.update()
        if gap:
            model.setParam('MIPgap', gap)
        if time_limit:
            model.setParam(GRB.Param.TimeLimit, time_limit)
        if verbose:
            model.setParam('OutputFlag', 1)
        else:
            model.setParam('OutputFlag', 0)
        model.setParam('LogFile', './logs/gurobi.log')
        # model.write("./logs/model.lp")

        start = time.time()
        model.optimize()
        end = time.time()
        comp_time = end - start
        
        
        
        sol = [0] * dict_data['Order']
        of = -1
        if model.status == GRB.Status.OPTIMAL:
           # for w in scenarios:
            for i in nodes:  
                grb_var = model.getVarByName(
                    f"Z[{i}]"
                )
                sol[i] = int(grb_var.X)
            of = round(model.getObjective().getValue(),4)
        return of, sol, comp_time

    def solve_deterministic(
        self, dict_data, reachability,time_limit=None,
        gap=None, verbose=False
    ):
        nodes = range(dict_data['Order'])

        problem_name = "LargeSI"
        logging.info("{}".format(problem_name))
        # logging.info(f"{problem_name}")

        model = gp.Model(problem_name)
        X = model.addVars(
            dict_data['Order'],
            lb=0,
            ub=1,
            vtype=GRB.INTEGER,
            name='X'
        )

        Z = model.addVars(
            dict_data['Order'],
            lb=0,
            ub=1,
            vtype=GRB.INTEGER,
            name='Z'
        )

        p=1
        obj_funct = p * gp.quicksum(X[i] for i in nodes)
            
        model.setObjective(obj_funct, GRB.MAXIMIZE)

        model.addConstr(
            gp.quicksum( Z[i] for i in nodes) <= dict_data['K'],
            f"Constraint on starting seed"
        )



        for i in nodes:
            model.addConstr(
                        X[i] <= gp.quicksum(Z[j] for j in reachability[i])
            )

        model.update()
        if gap:
            model.setParam('MIPgap', gap)
        if time_limit:
            model.setParam(GRB.Param.TimeLimit, time_limit)
        if verbose:
            model.setParam('OutputFlag', 1)
        else:
            model.setParam('OutputFlag', 0)
        model.setParam('LogFile', './logs/gurobi.log')
        # model.write("./logs/model.lp")

        start = time.time()
        model.optimize()
        end = time.time()
        comp_time = end - start
        
        
        
        sol = [0] * dict_data['Order']
        of = -1
        if model.status == GRB.Status.OPTIMAL:
           # for w in scenarios:
            for i in nodes:  
                grb_var = model.getVarByName(
                    f"Z[{i}]"
                )
                sol[i] = int(grb_var.X)
            of = round(model.getObjective().getValue(),4)
        return of, sol, comp_time
