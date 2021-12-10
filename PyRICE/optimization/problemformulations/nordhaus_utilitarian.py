"""
Running this script will run an optimization for the problem formulation that uses the Nordhaus damage function and
the utilitarian social welfare function.
"""

from PyRICE.optimization.problem_formulation import run_optimization
from PyRICE.model.enumerations import *


if __name__ == '__main__':

    run_optimization(damage_function=DamageFunction.NORDHAUS,
                     welfare_function=WelfareFunction.UTILITARIAN,
                     nfe=100000,
                     saving_results=True,
                     with_convergence=True)
