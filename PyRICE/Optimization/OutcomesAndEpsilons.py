from ema_workbench import ScalarOutcome
from Model.Enumerations import WelfareFunction


def get_outcomes_for_years(outcome_name, years_list, direction):
    """
    Return a list of outcomes with their proper names (including years) and their direction of optimization.
    """

    outcomes = []

    for year in years_list:
        outcome_name_with_year = outcome_name + ' ' + str(year)
        o = ScalarOutcome(outcome_name_with_year, direction)
        outcomes.append(o)

    return outcomes


def get_outcomes_to_optimize(outcomes_maximize_names, outcomes_minimize_names, years_optimize):
    """
    Return all the outcomes that should be optimized.
    """

    outcomes_optimize = []

    for outcome_name in outcomes_maximize_names:
        outcomes_optimize += get_outcomes_for_years(outcome_name, years_optimize, ScalarOutcome.MAXIMIZE)

    for outcome_name in outcomes_minimize_names:
        outcomes_optimize += get_outcomes_for_years(outcome_name, years_optimize, ScalarOutcome.MINIMIZE)

    return outcomes_optimize


def get_outcomes_to_info(outcomes_info_names, outcomes_optimize_names, years_optimize, years_info):
    """
    Return all the outcomes that should not be optimized but just presented as info.
    """

    outcomes_info = []

    for outcome_name in outcomes_info_names:
        outcomes_info += get_outcomes_for_years(outcome_name, years_optimize + years_info, ScalarOutcome.INFO)

    # Add remaining variables
    for outcome_name in outcomes_optimize_names:
        outcomes_info += get_outcomes_for_years(outcome_name, years_info, ScalarOutcome.INFO)

    return outcomes_info


def get_relevant_outcomes(outcomes_all_names, outcomes_maximize_names, outcomes_minimize_names,
                          outcomes_maximize_aggregated, outcomes_minimize_aggregated, years_optimize, years_info,
                          outcomes_info_aggregated):
    """
    This is a helper function. It returns the outcomes given a specification of all the above variables.
    """

    # Outcomes that should be optimized
    outcomes_optimize = []

    for outcome in outcomes_maximize_aggregated:
        outcomes_optimize.append((ScalarOutcome(outcome, ScalarOutcome.MAXIMIZE)))

    for outcome in outcomes_minimize_aggregated:
        outcomes_optimize.append((ScalarOutcome(outcome, ScalarOutcome.MINIMIZE)))

    outcomes_optimize += get_outcomes_to_optimize(outcomes_maximize_names, outcomes_minimize_names, years_optimize)

    # Outcomes that should only be displayed (i.e., not optimized)
    outcomes_info_names = list(set(outcomes_all_names)
                               - set(outcomes_maximize_names)
                               - set(outcomes_minimize_names))

    outcomes_info = []
    for outcome in outcomes_info_aggregated:
        outcomes_info.append((ScalarOutcome(outcome, ScalarOutcome.INFO)))

    outcomes_info += get_outcomes_to_info(outcomes_info_names,
                                         outcomes_minimize_names + outcomes_maximize_names,
                                         years_optimize,
                                         years_info)

    # Put them all together
    outcomes = outcomes_optimize + outcomes_info

    return outcomes


def get_epsilons(outcomes_all_optimize, dict_epsilons):
    epsilons = []
    for outcome_name in outcomes_all_optimize:
        epsilon = dict_epsilons[outcome_name]
        epsilons.append(epsilon)

    return epsilons


def get_outcomes_and_epsilons(welfare_function=WelfareFunction.UTILITARIAN):
    """
    Returns a list of outcomes and epsilons for the EMA workbench. The outcomes depend on:
        - the welfare function
        - the years that you are interested in, both for
            - optimization
            - just for info
        - which outcomes you find relevant

    :params:
        welfare_function: WelfareFunction

    :return:
        list of outcome variables and a list of epsilon values.
    """

    outcomes = []
    epsilons = []

    dict_epsilons = {
        'Total Aggregated Utility': 10,
        'Utility': 1,
        'Lowest income per capita': 0.02,
        'Intratemporal utility GINI': 0.001,
        'Total Output': 1.0,
        'Atmospheric Temperature': 0.1,
        'Highest climate impact per capita': 0.01,
        'Intratemporal impact GINI': 0.01,
        'Damages': 0.4,
        'Industrial Emission': 0.1,
        'Population under threshold': 1,
        'Distance to threshold': 0.0001
    }

    # Relevant years
    years_optimize = [2035, 2055, 2075]
    years_info = [2105, 2205, 2305]

    # All relevant outcome variable names
    outcomes_all_names = ['Damages', 'Utility', 'Intratemporal utility GINI', 'Intratemporal impact GINI',
                          'Lowest income per capita', 'Highest climate impact per capita', 'Distance to threshold',
                          'Population under threshold', 'Atmospheric Temperature', 'Industrial Emission', 'Total Output'
                          ]

    if welfare_function.__eq__(WelfareFunction.UTILITARIAN):

        outcomes_maximize_names = ['Utility']
        outcomes_minimize_names = []
        outcomes_maximize_aggregated = ['Total Aggregated Utility']
        outcomes_minimize_aggregated = []
        outcomes_info_aggregated = []

        # Create epsilons list with only relevant epsilons
        outcomes_all_optimize = outcomes_maximize_names + outcomes_minimize_names + outcomes_maximize_aggregated + outcomes_minimize_aggregated
        epsilons = get_epsilons(outcomes_all_optimize, dict_epsilons)

        outcomes = get_relevant_outcomes(outcomes_all_names, outcomes_maximize_names, outcomes_minimize_names,
                                         outcomes_maximize_aggregated, outcomes_minimize_aggregated, years_optimize,
                                         years_info, outcomes_info_aggregated)

    elif welfare_function.__eq__(WelfareFunction.SUFFICIENTARIAN):

        outcomes_maximize_names = []
        outcomes_minimize_names = ['Distance to threshold', 'Population under threshold']
        outcomes_maximize_aggregated = ['Total Aggregated Utility']
        outcomes_minimize_aggregated = []
        outcomes_info_aggregated = []

        # Create epsilons list with only relevant epsilons
        outcomes_all_optimize = outcomes_maximize_names + outcomes_minimize_names + outcomes_maximize_aggregated + outcomes_minimize_aggregated
        epsilons = get_epsilons(outcomes_all_optimize, dict_epsilons)

        outcomes = get_relevant_outcomes(outcomes_all_names, outcomes_maximize_names, outcomes_minimize_names,
                                         outcomes_maximize_aggregated, outcomes_minimize_aggregated, years_optimize,
                                         years_info, outcomes_info_aggregated)

    elif welfare_function.__eq__(WelfareFunction.PRIORITARIAN):

        # Outcomes that should be optimized
        outcomes_maximize_names = ['Lowest income per capita']
        outcomes_minimize_names = ['Highest climate impact per capita']
        outcomes_maximize_aggregated = []
        outcomes_minimize_aggregated = []
        outcomes_info_aggregated = ['Total Aggregated Utility']

        # Create epsilons list with only relevant epsilons
        outcomes_all_optimize = outcomes_maximize_names + outcomes_minimize_names + outcomes_maximize_aggregated + outcomes_minimize_aggregated
        epsilons = get_epsilons(outcomes_all_optimize, dict_epsilons)

        outcomes = get_relevant_outcomes(outcomes_all_names, outcomes_maximize_names, outcomes_minimize_names,
                                         outcomes_maximize_aggregated, outcomes_minimize_aggregated, years_optimize,
                                         years_info, outcomes_info_aggregated)

    elif welfare_function.__eq__(WelfareFunction.EGALITARIAN):

        # Outcomes that should be optimized
        outcomes_maximize_names = []
        outcomes_minimize_names = ['Intratemporal utility GINI', 'Intratemporal impact GINI 2055']
        outcomes_maximize_aggregated = []
        outcomes_minimize_aggregated = []
        outcomes_info_aggregated = ['Total Aggregated Utility']

        # Create epsilons list with only relevant epsilons
        outcomes_all_optimize = outcomes_maximize_names + outcomes_minimize_names + outcomes_maximize_aggregated + outcomes_minimize_aggregated
        epsilons = get_epsilons(outcomes_all_optimize, dict_epsilons)

        outcomes = get_relevant_outcomes(outcomes_all_names, outcomes_maximize_names, outcomes_minimize_names,
                                         outcomes_maximize_aggregated, outcomes_minimize_aggregated, years_optimize,
                                         years_info, outcomes_info_aggregated)

    return outcomes, epsilons


if __name__ == '__main__':

    results = get_outcomes_and_epsilons(welfare_function=WelfareFunction.UTILITARIAN)
    outcomes_list, eps = results

    print('Outcomes:')
    for out in outcomes_list:
        print(f'Outcome name: {out.name},\t optimization direction: {out.kind}')

    print('\nEpsilons:')
    for e in eps:
        print(f'Epsilon: {e}')
