from typing import List
import numpy as np
from enum import IntEnum
    
class Sign(IntEnum):
    POSITIVE = 5
    NEGATIVE = -5
    UNDEFINED = -10

class Factor:
    def __init__(self, title: str, solution_variables: List[str],
                 given_variables: List[str], values: List[float]) -> None:
        self.title = title
        self.solution_variables = solution_variables
        self.given_variables = given_variables
        self.variables = given_variables + solution_variables
        self.values = values
        self.table = self.generate_table(self.variables, values)

    def generate_table_skeleton(self, variables: List[str]) -> np.ndarray:
        num_variables = len(variables)
        num_rows = 2**num_variables
        num_cols = num_variables + 1
        table = np.zeros([num_rows, num_cols])
        table.fill(Sign.UNDEFINED)
        for i in range(len(variables)):
            combination_len = 2**(num_variables - i)//2
            for j in range(0, num_rows, combination_len*2):
                table[j:combination_len+j, [i]] = Sign.POSITIVE
                table[combination_len+j:2*combination_len+j, [i]] = Sign.NEGATIVE
        return table
        
    def generate_table(self, variables: List[str], values: List[float]) -> np.ndarray:
        table = self.generate_table_skeleton(variables)
        table[:, -1] = values
        return table

    def print_factor(self) -> None:
        print()
        for row in self.table:
            for i, cell in enumerate(row):
                if cell == Sign.POSITIVE:
                    print('{:^10s}'.format("+" + self.variables[i].lower()), end='|')
                elif cell == Sign.NEGATIVE:
                    print('{:^10s}'.format("-" + self.variables[i].lower()), end='|')
                else:
                    cell_value = "{:^.5f}".format(cell) 
                    print('{:^10s}'.format(cell_value), end='|\n')

    def remove_var(self, variable: str):
        self.variables.remove(variable)
        self.safe_remove_list(self.given_variables, variable)
        self.safe_remove_list(self.solution_variables, variable)

    @staticmethod
    def safe_remove_list(input_list: list, value):
        try:
            input_list.remove(value)
        except ValueError:
            pass

    def observe_var(self, variable: str, value: Sign) -> None:
        if variable not in self.variables:
            return
        index = self.variables.index(variable)
        self.table = self.table[self.table[:, index] == value]
        index = self.variables.index(variable)
        self.table = np.delete(self.table, index, axis=1)
        self.remove_var(variable)

    def normalize(self) -> None:
        sum_of_vals = sum(self.table[:, -1])
        self.table[:, -1] /= sum_of_vals
    
    def sumout(self, variable: str) -> None:
        if variable not in self.variables:
            return
        index = self.variables.index(variable)
        self.table = np.delete(self.table, index, axis=1)
        self.remove_var(variable)
        summed_out = self.generate_table_skeleton(self.variables)
        summed_out[:, -1] = 0
        for row1 in summed_out:
            for row2 in self.table:
                if (row1[:-1] == row2[:-1]).all():
                    row1[-1] = row1[-1] + row2[-1]
        self.table = summed_out

    @staticmethod
    def multiply(factor1, factor2):
        new_solution_vars = factor1.solution_variables + \
        [item for item in factor2.solution_variables if item not in factor1.solution_variables]
        new_given_vars = [item for item in factor2.given_variables if item not in new_solution_vars]
        new_prob_list = []
        for row1 in factor1.table:
            for row2 in factor2.table:
                if Factor.is_valid_row_multiply(factor1, factor2, row1, row2):
                    # print('{0} {1}'.format(row1, row2))
                    new_prob_list.append(row1[-1] * row2[-1])

        return Factor("no title", new_solution_vars, new_given_vars, new_prob_list)

    @staticmethod
    def is_valid_row_multiply(factor1, factor2, row1, row2) -> bool:
        for i, var1 in enumerate(factor1.variables):
            for j, var2 in enumerate(factor2.variables):
                if var1 == var2 and row1[i] != row2[j]:
                    return False
        return True


## Some testing code for factor methods

x = Factor('title', ['r'], [], [0.1, 0.9])
x2 = Factor('title', ['t'], ['r'], [0.8, 0.2, 0.1, 0.9])

multi = Factor.multiply(x, x2)
multi.print_factor()

test2 = Factor('x2', ['l'], ['t'], [0.3, 0.7, 0.1, 0.9])

multi = Factor.multiply(multi, test2)
multi.print_factor()


# print("\nInitial factor")
# test.print_factor()
#
# test.observe_var("Ron", Sign.NEGATIVE)
# print("\nAfter observing -ron")
# test.print_factor()
#
# test.normalize()
# print("\nAfter normalizing")
# test.print_factor()
#
# test.sumout("Mike")
# print("\nAfter summing out mike")
# test.print_factor()