from Factor import Factor


def observe(factor: Factor, variable: str, value: bool):
    """
    Restrict a variable to some value in a given factor
    :param factor:
    :param variable:
    :param value:
    :return:
    """
    if variable in factor.solution_vars or variable in factor.given_vars:
        # remove rows that don't have var set to value
        rows_to_delete = []
        # if len(factor.given_vars) > 0 and variable in factor.given_vars:
        for index, row in enumerate(factor.prob_table):
            if not row[factor.vars_index_list[variable]].value == value:
                rows_to_delete.append(index)

        factor.prob_table = [i for j, i in enumerate(factor.prob_table)
                             if j not in rows_to_delete]

        # remove the variable from the remaining rows of prob_table
        for row in factor.prob_table:
            del row[factor.vars_index_list[variable]]

        safe_remove_list(factor.given_vars, variable)
        safe_remove_list(factor.solution_vars, variable)

        # update vars_index_list to match changes done above
        del factor.vars_index_list[variable]
        for var in factor.given_vars:
            factor.vars_index_list[var] -= 1


def multiply(factor1: Factor, factor2: Factor):
    """
    Multiply two factors
    :param factor1: should have no given vars
    :param factor2:
    :return:
    """
    if len(factor1.given_vars) != 0:
        print('Incorrect use of multiply')
        return None

    new_factor_given_vars = []  # givens of factor2 - stuff from sol_vars
    new_factor_sol_vars = []  # all of factor1 + factor2 sols

    # start by checking that a solution var of one factor is a given var
    #  in the other?

    return factor1


def sumout(factor: Factor, variable: str):
    """
    Sums out a variable in a given factor
    Only works on 'and' factors (P(x,y,z)) not givens (P(x|y,z))
    :param factor:
    :param variable:
    :return:
    """
    # remove rows that don't have var set to value
    rows_to_delete = []
    probs_to_add = []
    # if len(factor.given_vars) > 0 and variable in factor.given_vars:
    for index, row in enumerate(factor.prob_table):
        if row[factor.vars_index_list[variable]].value:
            rows_to_delete.append(index)
            probs_to_add.append(row[len(row) - 1])

    factor.prob_table = [i for j, i in enumerate(factor.prob_table)
                         if j not in rows_to_delete]

    # remove the variable from the remaining rows of prob_table
    for index, row in enumerate(factor.prob_table):
        row[len(row) - 1] += probs_to_add[index]
        del row[factor.vars_index_list[variable]]

    safe_remove_list(factor.given_vars, variable)
    safe_remove_list(factor.solution_vars, variable)

    # update vars_index_list to match changes done above
    del factor.vars_index_list[variable]
    for var in factor.given_vars:
        factor.vars_index_list[var] -= 1


def normalize(factor: Factor):
    """
    Normalize a factor by dividing each entry by the sum of all the entries.
    This is useful when the factor is a distribution (i.e. sum of the
    probabilities must be 1).
    :param factor:
    :return:
    """
    total_sum = 0
    for row in factor.prob_table:
        total_sum += row[len(row) - 1]

    for row in factor.prob_table:
        row[len(row) - 1] = row[len(row) - 1] / total_sum


def inference(factor_list, query_variables, ordered_list_of_hidden_variables,
              evidence_list):
    """
    Too long to write here
    :param factor_list:
    :param query_variables:
    :param ordered_list_of_hidden_variables:
    :param evidence_list:
    :return:
    """
    # restrict factors based on evidence
    for factor in factor_list:
        for evidence_var, evidence_value in evidence_list:
            observe(factor, evidence_var, evidence_value)

    # remove any empty factors

    # multiply all factors (early marginalization??)

    # sum out hidden variables


def safe_remove_list(input_list: list, value):
    """
    Deletes an entry from a list without throwing the ValueError exception
    in case the entry is not in the set

    :param input_list: set from which the entry has to be removed
    :param value: the set entry to be removed
    """
    try:
        input_list.remove(value)
    except ValueError:
        pass

   # +x3    | 0.90317  |
   # -x3    | 0.09683  |

#   var elimination
# for var in ordered_list_of_hidden_variables:
#     factors_to_multiply = []
#     for factor in factor_list[:]:
#         if var in factor.variables:
#             factor_list.remove(factor)
#             factors_to_multiply.append(factor)
#
#     joined_factor = factors_to_multiply[0]
#     for i in range(1, len(factors_to_multiply)):
#         joined_factor = Factor.multiply(joined_factor, factors_to_multiply[i])
#     joined_factor.sumout(var)
#     factor_list.append(joined_factor)

