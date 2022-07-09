from evpy.wrappers.facade.kernel import Kernel


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
        self.__convergence_time = None

    def _get_convergence_time(self):
        return self.__convergence_time

    def _set_convergence_time(self, time):
        self.__convergence_time = time

    def _get_fitness(self):
        return self.__get_fitness

    def _get_kernel(self):
        return self.__kernel

    def _get_fittest(self):
        return self.__fittest

    def _set_fittest(self, value):
        self.__fittest = value

    def _get_max_fitness(self):
        return self.__max_fitness

    def _set_max_fitness(self, value):
        self.__max_fitness = value

    def _add_to_memory(self, value):
        self.__memory.append(value)

    def _get_memory(self):
        return self.__memory

    def _get_current(self):
        return self.__current_population

    def _set_current(self, value):
        self.__current_population = value
