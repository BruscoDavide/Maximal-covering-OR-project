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
        
        #obj_funct = gp.quicksum(p * gp.quicksum(X[i][j] for j in n_scenarios) for i in nodes)

        obj_funct = 0
        for w in scenarios:
            obj_funct += gp.quicksum(X[i,w] for i in nodes)
            obj_funct *= p


        # for s in scenarios:
        #     obj_funct += gp.quicksum(reward[i, s] * Y[i, s] for i in items)/(n_scenarios + 0.0)
        model.setObjective(obj_funct, GRB.MAXIMIZE)

        model.addConstr(
            gp.quicksum( Z[i] for i in nodes) <= dict_data['K'],
            f"Constraint on starting seed"
        )

        model.addConstr(
            X[i,w] <= gp.quicksum(Z[j] for j in reachability[i][:][w]) for i in nodes for j in scenarios
        )

        '''
        model.addConstr(
            for w in scenarios:
                for i in nodes:
                    ext_scenario=reachability[:][:][w]
                    X[i,w] <= gp.quicksum(Z[j] for j in ext_scenario[i][:])
        )

        
        for s in scenarios:
            model.addConstr(
                gp.quicksum(dict_data['sizes_ss'][i] * Y[i, s] for i in ) <= dict_data['max_size_ss'],
                f"volume_limit_ss_{s}"
            )
        for i in items:
            model.addConstr(
                gp.quicksum(Y[i, s] for s in scenarios) <= n_scenarios * X[i],
                f"link_X_Y_for_item_{i}"
            )
            '''
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
            for i in nodes:
                grb_var = model.getVarByName(
                    f"X[{i}]"
                )
                sol[i] = grb_var.X
            of = model.getObjective().getValue()
        return of, sol, comp_time
