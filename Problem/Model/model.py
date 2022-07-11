from Problem.rectangle import Rect
from Problem.rectangleCoordinates import rectangleCoordinates
from Problem.Model.fitness_wrapper import Fitness
from Problem.front_line import FrontLine

from evpy.genetic_operators.mutators.bimutators import exchange_mutation
from evpy.genetic_operators.recombination.discrete import discrete_unique
from evpy.genetic_operators.selectors.parent_selection import random_couple

from evpy.wrappers.facade.kernel_factory import KernelFactory
from Problem.Model.solver import Solver
import warnings

class Model:
    def __init__(self):
        self.band_width = 0     # W
        self.free_area_dim = 0  # разряды площади оставшейся
        self.filled_area = 0
        self.rectangles = []    # rectangles

        self.fitness = None
        self.solver = None
        self.send_data = None
        
        self.T = 1
        self.p_mut = 0.5
        self.p_gen_mut = 0.5

    def set_solver(self):
        builder = KernelFactory()
        _kernel = builder.build_kernel(exchange_mutation, discrete_unique, None, random_couple)
        self.solver = Solver(_kernel, self.fitness, self.rectangles, len(self.rectangles), len(self.rectangles))

        self.solver._clear_memory()

    def solve(self):
        result = self.solver.evaluate(T=1)
        # length, waste = self.decode(result[0][0].get_fittest().get_genotype())
        # result.set_length(length)
        # result.set_waste(waste)
        self.send_data(result)

    def decode(self, genotype):
        coordinates = []
        front = []
        rectangle = self.rectangles[genotype[0] - 1]
        if self.band_width != rectangle.get_height():
            front.append(FrontLine(self.band_width, rectangle.get_height(), 0))
        front.append(FrontLine(rectangle.get_height(), 0, rectangle.get_width()))
        coordinates.append(rectangleCoordinates(0, 0, rectangle.get_width(), rectangle.get_height()))
        front.sort(key=lambda n: n.x)
        # print(genotype)
        for gene in genotype[1:]:
            rectangle = self.rectangles[gene - 1]
            for i in range(len(front)):
                if front[i].left_y - front[i].right_y > rectangle.get_height():  # fits on the line
                    coordinates.append(rectangleCoordinates(front[i].x, front[i].right_y, rectangle.get_width(), rectangle.get_height()))
                    front[i].right_y += rectangle.get_height()
                    front.append(FrontLine(front[i].right_y, front[i].right_y - rectangle.get_height(),
                                      front[i].x + rectangle.get_width()))
                    break

                elif (front[i].left_y - front[i].right_y) == rectangle.get_height():  # fits on the line (same height)
                    coordinates.append(rectangleCoordinates(front[i].x, front[i].right_y, rectangle.get_width(), rectangle.get_height()))
                    front[i].x += rectangle.get_width()
                    break

                elif i == (len(front) - 1):  # top line, doesn't fit on it
                    coordinates.append(rectangleCoordinates(front[i].x, 0, rectangle.get_width(), rectangle.get_height()))
                    if front[i].left_y > rectangle.get_height():
                        front[i].right_y = rectangle.get_height()
                    newX = front[i].x + rectangle.get_width()
                    front = list(filter(lambda n: n.left_y > rectangle.get_height(), front))
                    front.append(FrontLine(rectangle.get_height(), 0, newX))
                    if rectangle.get_height() != self.band_width:
                        for j in range(len(front)):
                            if (front[j].right_y < rectangle.get_height()):
                                front[j].right_y = rectangle.get_height()
                                break
                    break

                else:  # doesn't fit on the line
                    collision = False
                    rightBorder = front[i].right_y + rectangle.get_height()
                    if rightBorder <= self.band_width:
                        for j in range(i + 1, len(front)):  # check top lines for collision
                            if (front[j].right_y < rightBorder and front[j].right_y >= front[i].left_y):
                                collision = True
                                break
                        if not collision:  # no collision, cover by 'shadow'
                            coordinates.append(rectangleCoordinates(front[i].x, front[i].right_y, rectangle.get_width(), rectangle.get_height()))
                            newX = front[i].x + rectangle.get_width()
                            newHeight = front[i].right_y + rectangle.get_height()
                            front = list(filter(lambda n: n.left_y > newHeight or n.left_y <= front[i].right_y, front))
                            front.append(FrontLine(newHeight, newHeight - rectangle.get_height(), newX))

                            if newHeight != self.band_width:
                                for j in range(len(front)):
                                    if (front[j].right_y < rectangle.get_height()):
                                        front[j].right_y = rectangle.get_height()
                                        break
                            break
            front.sort(key=lambda n: n.x)

        LineLength = front[-1].x
        FreeArea = self.band_width * LineLength - self.filled_area
        return LineLength, FreeArea, coordinates

    def process_data(self, band_width: int, rects: list):
        self.band_width = band_width
        max_length, rect_area = 0, 0

        self.rectangles = []

        for i in range(1, len(rects), 2):
            self.rectangles.append(Rect(rects[i-1], rects[i]))
            max_length += rects[i-1]
            rect_area += rects[i-1] * rects[i]

        self.filled_area = rect_area
        self.free_area_dim = 10 ** len((str(max_length)))

        self.set_algorithm()

    def set_algorithm(self):
        if self.rectangles:
            self.fitness = Fitness(self.rectangles, self.filled_area, self.free_area_dim, self.band_width,
                                   self.decode)

        self.set_solver()

    def set_send_data(self, slot):
        self.send_data = slot

    def get_parameters(self):
        return {'T': [self.T, 1, 200, True], 'p_mut': [self.p_mut, 0.01, 1.0, False],
                'p_gen_mut': [self.p_gen_mut, 0.01, 1.0, False]}
    
    def set_parameter(self, key, val):
        print('set_parameter: ', key, val)
        if key == 'T':
            self.T = val
        elif key == 'p_mut':
            self.p_mut = val
        elif key == 'p_gen_mut':
            self.p_gen_mut = val
        else:
            warnings.warn("Warning: model has no such parameter")
    
    def get_band_width(self):
        return self.band_width