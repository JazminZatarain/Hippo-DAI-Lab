# Problem Formulations for Optimization


## Outcomes and Epsilons
This folder contains a script `OutcomesAndEpsilons.py` which contains a function to define the relevant outcomes for optimization. 


## Problem Formulations

The file `ProblemFormulation.py` contains the function `run_optimization` which can be used to run an optimization. Furthermore, the folder `ProblemFormulations` contains four alternative problem formulations – each file name consist of the name of the damage function plus the ethical principle:

- `NordhausUtilitarian.py`
- `NordhausSufficientarian.py`
- `WeitzmanUtilitarian.py`
- `WeitzmanSufficientarian.py`

Run any of these scripts to run the corresponding optimization and decide whether to save the results and/or convergence data.

## Model Results

The results of the optimization processes are saved into the folder `ModelResults`. The csv files have a naming convention that combines information about the optimization with the following order:

- results or convergence
- damage function name
- welfare function name
- used number of function evaluations (nfe)


E.g., running the optimization with:

- `damage_function = DamageFunction.NORDHAUS`
- `welfare_function = WelfareFunction.UTILITARIAN`
- `nfe = 10000`
- `with_convergence = True`

This would result in two files:

- `results_NORDHAUS_UTILITARIAN_runs_10000.csv`
- `convergence_NORDHAUS_UTILITARIAN_runs_10000.csv`