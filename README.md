# Influence Maximization Problem

This IMP problem resolution program requires:

1. Python 3.6 or greater
1. gurobi
1. Collection library



## Run the code:

To run the code it is required to launch the main file
```
python3 main.py
```
The program can run on 3 type of different graphs, two not customizable one instead letting the user to set the graph order.
The first graph is a ad-hoc graph done to test the model correctness working only with 14 nodes.
The second graph is a scale free that can be created with an arbitrary number of nodes which has to be set as parameter in "sim_settings.json" file.
The third one is a graph obtained from a third party site. To run this code it is required to have the "librec-filmtrust-trust" folder in the "dataset" folder.

To decide which type of graph to use, it is required to set: "curated", "random" or "konect" at the "Graph_type" in "sim_settings.json" , then the "Instance" class will provide the graph.

## Problem:

The program tries to solve the IMP problem as:
$$
\max \sum_{\omega \in \mathcal{\Omega}} p_i  \sum_{i\in \mathcal{N}}x_{i}^{\omega}
$$
subject to:
$$
x_{i}^{\omega} \leq \sum_{j \in \mathcal{R(\omega,j)}}z_{j}
$$

$$
\sum_{i \in \mathcal{V}}z_{i} \leq K
$$

$$
x_{i}^{\omega}, z_i \in \{0, 1\}\ \ \ \forall\ i \in \mathcal{I}, \forall\ \omega \in \mathcal{\Omega}
$$



The problem is solved with Gurobi and with a fine tuned heuristic method. The Gurobi resolution is contained in the "LargeScaleInfluence.py" in the "solver" folder , while the heuristic is in "FirstHeuristic.py" in the "heuristic" folder.
The main contains both the method running, printing the result for a immediate comparison.

The "Sampler" class creates the R(i,w) instances, sampling n_scenarios rows for the selected graphs.

After the problem solution, the in sample stability and out of sample are performed, plotting the solutions in function of the number of scenarios used for obtaining the seed set.

After the system stability, the comparison between the out of sample results and a mean seed set is performed. The mean service set is computed in function of an hyperparameter.

Those testes can be found in the "Tester" class in the "simulator" folder.

