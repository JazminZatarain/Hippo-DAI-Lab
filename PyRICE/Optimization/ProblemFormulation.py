# Imports

from Model.PyRICE import PyRICE
from Model.Enumerations import *
from Optimization.OutcomesAndEpsilons import get_outcomes_and_epsilons
import os

# EMA

from ema_workbench.em_framework.optimization import (HyperVolume, EpsilonProgress)
from ema_workbench import (Model, RealParameter, IntegerParameter, MultiprocessingEvaluator, ema_logging, Constant)
from ema_workbench.em_framework.optimization import EpsNSGAII

ema_logging.log_to_stderr(ema_logging.INFO)


def define_path_name(damage_function, welfare_function, nfe, prefix='results'):
    """
    Define path and file name such that it can be used to save results or covergence data.

    :params:
        damage_function: DamageFunction
        welfare_function: WelfareFunction
        nfe: integer
        prefix: string {'results', 'convergence'}
    """

    file_name = damage_function.name + '_' + \
                welfare_function.name + '_' + \
                prefix + '_' + \
                str(nfe) + \
                '.csv'

    folder = '/ModelResults/'
    directory = os.path.dirname(os.path.realpath(__file__))
    path = directory + folder + file_name

    return path


def run_optimization(damage_function=DamageFunction.NORDHAUS,
                     welfare_function=WelfareFunction.UTILITARIAN,
                     nfe=5000,
                     saving_results=False,
                     with_convergence=False):
    """
    This function runs an optimization with the PyRICE model.

    :params
        damage_function: DamageFunction (enum)
        welfare_function: WelfareFunction (enum)
        nfe: integer
        saving_results: Boolean
        with_concergence: Boolean
    """

    # Instantiate the model
    model_specification = ModelSpec.EMA

    model = PyRICE(model_specification=model_specification,
                   damage_function=damage_function,
                   welfare_function=welfare_function)

    model = Model('RICE', function=model)

    # Specify uncertainties
    model.uncertainties = [IntegerParameter('t2xco2_index', 0, 999),
                           IntegerParameter('t2xco2_dist', 0, 2),
                           RealParameter('fosslim', 4000, 13649),
                           IntegerParameter('scenario_pop_gdp', 0, 5),
                           IntegerParameter('scenario_sigma', 0, 2),
                           IntegerParameter('scenario_cback', 0, 1),
                           IntegerParameter('scenario_elasticity_of_damages', 0, 2),
                           IntegerParameter('scenario_limmiu', 0, 1)]

    # Set levers, one for each time step
    model.levers = [RealParameter('sr', 0.1, 0.5),
                    RealParameter('miu', 2065, 2300),
                    RealParameter('irstp', 0.001, 0.015)]

    # Specify outcomes
    model.outcomes, epsilons = get_outcomes_and_epsilons(welfare_function=welfare_function)

    # TODO: why are outcomes with info shown here but not in the results?
    for o in model.outcomes:
        print(f'outcome: {o.name}, \t direction: {o.kind}')

    model.constants = [Constant('model_specification', ModelSpec.EMA),
                       Constant('damage_function', DamageFunction.NORDHAUS),
                       Constant('welfare_function', WelfareFunction.UTILITARIAN),
                       Constant('precision', 10)]

    constraints = []

    # only needed on IPython console within Anaconda
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

    # Run optimization
    if with_convergence:

        # convergence_metrics = [HyperVolume.from_outcomes(model.outcomes), EpsilonProgress()]
        convergence_metrics = [EpsilonProgress()]

        with MultiprocessingEvaluator(model) as evaluator:

            results, convergence = evaluator.optimize(algorithm=EpsNSGAII,
                                                      nfe=nfe,
                                                      searchover='levers',
                                                      epsilons=epsilons,
                                                      convergence=convergence_metrics,
                                                      constraints=constraints)

            if saving_results:

                # Save results
                path = define_path_name(damage_function, welfare_function, nfe, prefix='results')
                results.to_csv(path)

                # Save convergence
                path = define_path_name(damage_function, welfare_function, nfe, prefix='convergence')
                convergence.to_csv(path)

    else:

        with MultiprocessingEvaluator(model) as evaluator:

            results = evaluator.optimize(algorithm=EpsNSGAII,
                                         nfe=nfe,
                                         searchover='levers',
                                         epsilons=epsilons,
                                         constraints=constraints)

            if saving_results:
                path = define_path_name(damage_function, welfare_function, nfe, prefix='results')
                results.to_csv(path)


if __name__ == '__main__':

    run_optimization(welfare_function=WelfareFunction.SUFFICIENTARIAN,
                     damage_function=DamageFunction.WEITZMAN,
                     nfe=20000,
                     saving_results=True,
                     with_convergence=True)
