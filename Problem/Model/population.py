from Problem.Model.cringe_solution import Solution


class Population:
    def __init__(self, population: list[Solution]):
        self.__species = tuple(population)

        self.__fittest = 0

    def get_fittest(self):
        return self.__species[self.__fittest]

    def set_fittest(self, index: int):
        self.__fittest = index

    def get_population(self):
        return self.__species
