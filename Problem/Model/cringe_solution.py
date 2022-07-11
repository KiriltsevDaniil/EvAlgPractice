class Solution:
    def __init__(self, rectangles: list, band_length: int = None, waste: int = None):
        self.__length = band_length
        self.__waste = waste
        self.rectangles = rectangles    # output sorted by indexes from fittest

        self.__population = None       # list of genotypes
        self.__fittest = None          # fittest genotype, aka best list of rect indexes
        self.__fitness = None
        self.__parents = None           # list of 2 previous Solutions

    def set_fittest(self, genotype: list):
        self.__fittest = genotype

    def get_fittest(self):
        return self.__fittest

    def set_population(self, population):
        self.__population = population

    def get_population(self):
        return self.__population

    def set_fitness(self, fitness_value: int):
        self.__fitness = fitness_value

    def get_fitness(self):
        return self.__fitness

    def set_parents(self, parents: list):
        self.__parents = parents

    def get_parents(self):
        return self.__parents

    def set_length(self, band_length):
        self.__length = band_length

    def get_length(self):
        return self.__length

    def set_waste(self, waste):
        self.__waste = waste

    def get_waste(self):
        return self.__waste
