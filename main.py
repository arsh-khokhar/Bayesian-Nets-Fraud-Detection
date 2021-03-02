class Factor:
    def __init__(size):
        print('2-D list + what it represents (ex P(x|r) or P(x,r))?')


def observe(factor, variable, value: bool):
    """
    Restrict a variable to some value in a given factor
    :param factor:
    :param variable:
    :param value:
    :return:
    """
    print('hello world')
    # if a factor is P(x|y) and we know that y, then we can reduce the factor
    #  to P(x) by only keeping the rows with y (and removing ones with -y)


def multiply(factor1, factor2):
    """
    Multiply two factors
    :param factor1:
    :param factor2:
    :return:
    """
    print('hello world')
    # need to validate the we can multiply these factors together
    #  (ex P(x) * P(y|x) is valid but P(x) * P(y|z) isn't)


def sumout(factor, variable):
    """
    Sums out a variable in a given factor
    :param factor:
    :param variable:
    :return:
    """
    # similar to observe, but instead we sum probabilities of rows that are the
    #  same (ex have var x set to -x)
    # only works on 'and' factors (P(x,y,z)) not givens (P(x|y,z))?


def normalize(factor):
    """
    Normalize a factor by dividing each entry by the sum of all the entries.
    This is useful when the factor is a distribution (i.e. sum of the
    probabilities must be 1).
    :param factor:
    :return:
    """
    print('hello world')


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
    print('hello world')
    # in theory just use the other functions to find the hidden var probs, in
    #  order of ordered_list_of_hidden_variables
