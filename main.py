from inference import inference
from var_elimination import Factor, Sign
import sys


def main():
    print(sys.path)
    factors = [Factor('title', ['A'], [], [0.1, 0.1]),
               Factor('title', ['B'], ['A'], [0.1, 0.1, 0.1, 0.1]),
               Factor('title', ['C'], [], [0.1, 0.1]),
               Factor('title', ['D'], ['A', 'B', 'C'],
                      [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
               Factor('title', ['E'], ['D'], [0.1, 0.1, 0.1, 0.1]),
               Factor('title', ['F'], ['D'], [0.1, 0.1, 0.1, 0.1]),
               Factor('title', ['G'], ['F', 'C'], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])]

    inference(factors, [], ['B', 'D', 'G', 'F'], [('C', Sign.POSITIVE)])


if __name__ == '__main__':
    main()
