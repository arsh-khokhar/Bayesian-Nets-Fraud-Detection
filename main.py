"""
    File name: main.py
    Author: Arsh Khokhar, Kiernan Wiese
    Date last modified: 19 March, 2021
    Python Version: 3.8

    This script contains the main function that calls inference.py to solve
    and show solutions a specific inference query. It parses command line
    arguments that specify which query to do.
"""

import sys

from Factor import Factor, Sign
from Inference import inference


def main() -> None:
    if len(sys.argv) <= 1:
        print('Usage: python main.py [1 or 2 for 2b part 1 and 2 respectively]')
        exit(-1)

    sim_to_run = sys.argv[1]

    factors = [Factor(['Trav'], [], [0.05, 0.95]),
               Factor(['Fraud'], ['Trav'], [0.01, 0.99, 0.004, 0.996]),
               Factor(['OC'], [], [0.7, 0.3]),
               Factor(['CRP'], ['OC'], [0.1, 0.9, 0.001, 0.999]),
               Factor(['FP'], ['Trav', 'Fraud'], [0.9, 0.1, 0.9, 0.1,
                                                  0.1, 0.9, 0.01, 0.99]),
               Factor(['IP'], ['OC', 'Fraud'], [0.02, 0.98, 0.01, 0.99,
                                                0.011, 0.989, 0.001, 0.999])]

    if sim_to_run == '1':
        inference(factors, ['Fraud'], ['Trav', 'FP', 'IP', 'OC', 'CRP'], [])
    else:
        inference(factors, ['Fraud'], ['Trav', 'OC'],
                  [('FP', Sign.POSITIVE), ('IP', Sign.NEGATIVE), ('CRP', Sign.POSITIVE)])


if __name__ == '__main__':
    main()
