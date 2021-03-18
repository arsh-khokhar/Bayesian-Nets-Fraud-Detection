from var_elimination import Factor
from typing import List


def print_all_factors(factor_list):
    for factor in factor_list:
        factor.print_representation()
        # factor.print_factor()
    print()


def inference(factor_list: List[Factor], query_variables: List[str],
              ordered_list_of_hidden_variables: List[str],
              evidence_list):  # List[(str, bool)]
    # restrict factors based on evidence
    for factor in factor_list[:]:
        for evidence_var, evidence_value in evidence_list:
            factor.observe_var(evidence_var, evidence_value)
        if len(factor.variables) == 0:
            factor_list.remove(factor)
    print('Initial factors:')
    print_all_factors(factor_list)

    #  inference by enumeration
    # joined_factor = factor_list[0]
    # for i in range(1, len(factor_list)):
    #     joined_factor = Factor.multiply(joined_factor, factor_list[i])
    # for var in ordered_list_of_hidden_variables:
    #     joined_factor.sumout(var)
    # joined_factor.normalize()
    # joined_factor.print_factor()

    #  var elimination
    for var in ordered_list_of_hidden_variables:
        factors_to_multiply = []
        for factor in factor_list[:]:
            if var in factor.variables:
                factor_list.remove(factor)
                factors_to_multiply.append(factor)

        joined_factor = factors_to_multiply[0]
        for i in range(1, len(factors_to_multiply)):
            joined_factor = Factor.multiply(joined_factor, factors_to_multiply[i])
        joined_factor.sumout(var)
        factor_list.append(joined_factor)
        print('After eliminating {0}:'.format(var))
        print_all_factors(factor_list)

    joined_factor = factor_list[0]
    for i in range(1, len(factor_list)):
        joined_factor = Factor.multiply(joined_factor, factor_list[i])

    joined_factor.normalize()
    joined_factor.print_representation()
    joined_factor.print_factor()
