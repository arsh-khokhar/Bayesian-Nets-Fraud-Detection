from var_elimination import Factor
import FactorFunctions
import math


TEST_FACTORS_FOR_OBSERVE = [
    (Factor('title', ['y'], ['x'], [0.5, 0.5, 0.1, 0.9]),
     'x', True, ['y'], []),
    (Factor('title', ['x', 'y'], ['z', 'a'], [0, 0.1, 0.2, 0.3, 0, 0.1, 0.2, 0.3,
                                    0, 0.1, 0.2, 0.3, 0, 0.1, 0.2, 0.3]),
     'z', False, ['x', 'y'], ['a']),
                              ]


def test_observe():
    for test_factor, observed_var, observed_val, new_sol_list, new_given_list \
            in TEST_FACTORS_FOR_OBSERVE:
        pre_observe_len = len(test_factor.prob_table)
        FactorFunctions.observe(test_factor, observed_var, observed_val)
        # the list should be half the size
        assert pre_observe_len/2 == len(test_factor.prob_table)
        # the var we observed should no longer be part of the factor
        assert observed_var not in test_factor.vars_index_list.keys()
        assert observed_var not in test_factor.given_vars
        assert test_factor.given_vars == new_given_list
        assert test_factor.solution_vars == new_sol_list


TEST_FACTORS_FOR_MULTIPLY = [
    (Factor('title', ['r'], [], [0.1, 0.9]),
     Factor('title', ['t'], ['r'], [0.8, 0.2, 0.1, 0.9]),
     Factor('title', ['r', 't'], [], [0.08, 0.02, 0.09, 0.81])),

    (Factor('title', ['r', 't'], [], [0.08, 0.02, 0.09, 0.81]),
     Factor('title', ['l'], ['t'], [0.3, 0.7, 0.1, 0.9]),
     Factor('title', ['r', 't', 'l'], [], [0.024, 0.056, 0.002, 0.018, 0.027, 0.063,
                                  0.081, 0.729])
     )
]


def test_multiply():
    for test_factor1, test_factor2, expected_result_factor \
            in TEST_FACTORS_FOR_MULTIPLY:
        new_factor = FactorFunctions.multiply(test_factor1, test_factor2)

        assert new_factor.given_vars == expected_result_factor.given_vars
        assert new_factor.solution_vars == expected_result_factor.solution_vars

        for index, row in enumerate(expected_result_factor.prob_table):
            assert math.isclose(row[len(row) - 1],
                                new_factor.prob_table[index][len(row) - 1])



TEST_FACTORS_FOR_SUMOUT = [
    (Factor('title', ['t', 'l'], [], [0.051, 0.119, 0.083, 0.747]),
     't', ['l'], []),
    (Factor('title', ['r', 't', 'l'], [], [0.024, 0.056, 0.002, 0.018, 0.027, 0.063, 0.081, 0.729]),
     't', ['r', 'l'], []),
    (Factor('title', ['a', 'b', 'c', 'd'], [], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]),
     'b', ['b', 'c', 'd'], []),
                              ]


def test_sumout():
    for test_factor, sum_var, new_sol_list, new_given_list \
            in TEST_FACTORS_FOR_SUMOUT:
        pre_observe_len = len(test_factor.prob_table)

        FactorFunctions.sumout(test_factor, sum_var)

        assert pre_observe_len/2 == len(test_factor.prob_table)


TEST_FACTORS_FOR_NORMALIZE = [
    Factor('title', ['x'], [], [1, 1]),
    Factor('title', ['x', 'y'], ['z', 'a'], [0, 0.1, 0.2, 0.3, 0, 0.1, 0.2, 0.3,
                                    0, 0.1, 0.2, 0.3, 0, 0.1, 0.2, 0.3]),
                              ]


def test_normalize():
    for test_factor in TEST_FACTORS_FOR_NORMALIZE:
        FactorFunctions.normalize(test_factor)
        total_sum = 0
        for row in test_factor.prob_table:
            total_sum += row[len(row) - 1]

        assert math.isclose(total_sum, 1)
