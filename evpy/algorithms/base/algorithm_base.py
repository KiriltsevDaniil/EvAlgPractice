from evpy.commands.genetic_operators.wrappers.facade.kernel import Kernel


def make_base(kernel: Kernel, fitness):
    return AlgorithmBase(kernel, fitness)


# Base to build any algorithm upon
class AlgorithmBase:
    def __init__(self, kernel: Kernel, fitness):

        self.__get_fitness = fitness
        self.__kernel = kernel

        self.__memory = []
        self.__current_population = None
        self.__fittest = None
        self.__max_fitness = None
