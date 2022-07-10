from evpy.algorithms.base.algorithm import Algorithm


def make_parallel(archipelago: list, fitness_function: callable, rule: callable = None):
    return Parallel(archipelago, fitness_function, rule)


class Parallel(Algorithm):
    def __init__(self, archipelago: list, fitness_function: callable, rule: callable = None):
        super().__init__(fitness_function)

        self.__archipelago = archipelago
        self.__migration = rule

    def _get_archipelago(self):
        return self.__archipelago

    def _migrate(self):
        return self.__migration
