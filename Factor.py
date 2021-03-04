class Factor:
    def __init__(self, solution_vars: list, given_vars: list,
                 probabilities: list):
        #  need at least one solution var
        if len(solution_vars) > 0:
            #  will be useful later
            self.solution_vars = solution_vars
            self.given_vars = given_vars

            self.prob_table = []

            table_height = 2 ** (len(solution_vars) + len(given_vars))
            table_width = len(solution_vars) + len(given_vars) + 1

            for y in range(table_height):
                self.prob_table.append([])

            for x in range(table_width - 1):
                sign_flipper = table_height / (2 ** (x+1))
                curr_sign = False
                for y in range(table_height):
                    curr_var = solution_vars[x] if x < len(solution_vars) \
                        else given_vars[x-len(solution_vars)]

                    if y % sign_flipper == 0:
                        curr_sign = not curr_sign

                    self.prob_table[y].append(TableVariable(curr_var,
                                                            curr_sign))
            for y in range(table_height):
                self.prob_table[y].append(probabilities[y])

    def print_table(self):
        for row in self.prob_table:
            print('|', end='')
            for element in row:
                print(element, end='')
                print('|', end='')
            print('\n', end='')


class TableVariable:
    def __init__(self, var_nm: str, vl: bool):
        self.var_name = var_nm
        self.value = vl

    def __str__(self):
        return '{0}{1}'.format('+' if self.value else '-', self.var_name)
