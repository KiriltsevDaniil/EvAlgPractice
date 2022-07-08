from evpy.commands.genetic_operators.wrappers.facade.kernel import Kernel


def make_base(kernel: Kernel, fitness):
    return AlgorithmBase(kernel, fitness)


class AlgorithmBase:
    def __init__(self, kernel, fitness):

        self.__get_fitness = fitness
        self.__kernel = kernel

        self.__memory = []
        self.__fittest = None
        self.__max_fitness = None
