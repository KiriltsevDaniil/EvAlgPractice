from evpy.wrappers.decorators.command import Command

from Task.genetic_algorithm.solution import Solution


class Fitness(Command):
    def __init__(self, rectangles: list, filled_area: int, free_dim: int, band_width: int, decode: callable,
                 fitness_function=None,):

        if fitness_function is None:
            fitness_function = self.fitness

        super().__init__(fitness_function)

        self.band_width = band_width
        self.rectangles = rectangles
        self.filled_area = filled_area
        self.free_area_dim = free_dim

        self.decode = decode

    def fitness(self, individual: Solution):
        length, free_area, coordinates = self.decode(individual.get_genotype())
        individual.set_length(length)
        individual.set_waste(free_area)
        individual.set_coordinates(coordinates)

        return length + free_area * self.free_area_dim
