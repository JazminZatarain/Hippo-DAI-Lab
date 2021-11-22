from Optimization.ProblemFormulation import run_optimization
from Model.Enumerations import *


if __name__ == '__main__':

    run_optimization(damage_function=DamageFunction.NORDHAUS,
                     welfare_function=WelfareFunction.UTILITARIAN,
                     nfe=10000,
                     saving_results=True,
                     with_convergence=True)
