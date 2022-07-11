class Solution:
    def __init__(self, rectangles: list, genotype: list, index: int):
        self.__id = index
        self.__genotype = genotype
        self.__fitness = -1

        self.__parents = None
        self.__rectangles = rectangles
        self.__band_length = -1
        self.__waste = -1

    def get_id(self):
        return self.__id

    def get_genotype(self):
        return self.__genotype

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self, value: int):
        self.__fitness = value

    def get_parents(self):
        return self.__parents

    def set_parents(self, parents: list[list[int]]):
        self.__parents = parents

    def get_length(self):
        return self.__band_length

    def set_length(self, value: int):
        self.__band_length = value

    def get_waste(self):
        return self.__waste

    def set_waste(self, value: int):
        self.__waste = value

    def get_rectangles(self):
        return self.__rectangles
