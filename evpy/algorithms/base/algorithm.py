from Task.Logger.publisher import Publisher


def make_algorithm(fitness: callable):
    return Algorithm(fitness)


# Base to build any algorithm upon
class Algorithm(Publisher):
    def __init__(self, fitness: callable):
        super(Algorithm, self).__init__()
        self.__get_fitness = fitness

        self.__memory = []
        self.__fittest = None
        self.__max_fitness = None
        self.__convergence_time = None

    def _get_convergence_time(self):
        return self.__convergence_time

    def _set_convergence_time(self, time: float):
        self.__convergence_time = time

    def _get_fitness(self):
        return self.__get_fitness

    def _get_fittest(self):
        return self.__fittest

    def _set_fittest(self, value: list):
        self.__fittest = value

    def _get_max_fitness(self):
        return self.__max_fitness

    def _set_max_fitness(self, value: int):
        self.__max_fitness = value

    def _add_to_memory(self, value):
        self.__memory.append(value)

    def _get_memory(self):
        return self.__memory
