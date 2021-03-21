"""
    File name: Inference.py
    Author: Arsh Khokhar, Kiernan Wiese
    Date last modified: 19 March, 2021
    Python Version: 3.8

    This script contains functions to calculate inference and print factors
    as we go.
"""
from typing import List, Tuple
from Factor import Factor, Sign


def inference_by_enumeration(factor_list: List[Factor],
                             ordered_list_of_hidden_variables: List[str]):
    """
    Calculate P(factor_list | evidence_list) using inference by enumeration, after
    all of the evidence is observed
    This function is unused when doing inference

    :param factor_list: List of the factors we'll use
    :param ordered_list_of_hidden_variables: The order to sumout variables not in query_variables or evidence_list
    """
    joined_factor = factor_list[0]
    for i in range(1, len(factor_list)):
        joined_factor = Factor.multiply(joined_factor, factor_list[i])
    for var in ordered_list_of_hidden_variables:
        joined_factor.sumout(var)
    joined_factor.normalize()
    joined_factor.print_factor()


def var_elimination(factor_list: List[Factor], query_variables: List[str],
                    ordered_list_of_hidden_variables: List[str],
                    evidence_list: List[Tuple[str, Sign]]):
    """
    Calculate P(factor_list | evidence_list) using variable elimination, after
    all of the evidence is observed

    :param factor_list: List of the factors we'll use
    :param query_variables: We want to find this variables' probability
    :param ordered_list_of_hidden_variables: The order to sumout variables not in query_variables or evidence_list
    :param evidence_list: List of variables that we know the values of
    """
    for var in ordered_list_of_hidden_variables:
        # find out which factors contain var, remove them from factor_list
        factors_to_multiply = []
        for factor in factor_list[:]:
            if var in factor.variables:
                factor_list.remove(factor)
                factors_to_multiply.append(factor)

        # multiply all the removed factors together, then sumout var
        joined_factor = factors_to_multiply[0]
        for i in range(1, len(factors_to_multiply)):
            joined_factor = Factor.multiply(joined_factor, factors_to_multiply[i])
        joined_factor.sumout(var)

        if len(joined_factor.solution_variables) > 0:
            factor_list.append(joined_factor)
        print('After eliminating {0}:'.format(var))
        print_all_factors(factor_list)

    # multiply remaining factors together
    joined_factor = factor_list[0]
    for i in range(1, len(factor_list)):
        joined_factor = Factor.multiply(joined_factor, factor_list[i])

    joined_factor.normalize()

    final_factor = Factor(query_variables, [], joined_factor.table[:, -1], [], evidence_list)
    print('Solution:')
    final_factor.print_representation()
    final_factor.print_factor()


def print_all_factors(factor_list: List[Factor]) -> None:
    """
    Print a representation of all of the factors

    :param factor_list: The factors to print
    """
    for factor in factor_list:
        factor.print_representation()
        # factor.print_factor()
    print()


def inference(factor_list: List[Factor], query_variables: List[str],
              ordered_list_of_hidden_variables: List[str],
              evidence_list: List[Tuple[str, Sign]]) -> None:
    """
    Calculate P(factor_list | evidence_list) using variable elimination

    :param factor_list: List of the factors we'll use
    :param query_variables: We want to find this variables' probability
    :param ordered_list_of_hidden_variables: The order to sumout variables not in query_variables or evidence_list
    :param evidence_list: List of variables that we know the values of
    :return:
    """
    # restrict factors based on evidence
    for factor in factor_list[:]:
        for evidence_var, evidence_value in evidence_list:
            factor.observe_var(evidence_var, evidence_value)
        if len(factor.variables) == 0:
            factor_list.remove(factor)
    print('Initial factors:')
    print_all_factors(factor_list)

    #  inference by enumeration
    # inference_by_enumeration(factor_list, ordered_list_of_hidden_variables)

    #  var elimination
    var_elimination(factor_list, query_variables,
                    ordered_list_of_hidden_variables, evidence_list)
