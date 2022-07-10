from evpy.wrappers.decorators.command import Command
from Problem.rectangle import Rect
from Problem.front_line import FrontLine


class Fitness(Command):
    def __init__(self, rectangles: list, filled_area: int, free_dim: int, band_width: int, fitness_function=None,):
        if fitness_function is None:
            fitness_function = self.fitness

        super().__init__(fitness_function)

        self.band_width = band_width
        self.rectangles = rectangles
        self.filled_area = filled_area
        self.free_area_dim = free_dim

    def decode(self, genotype):
        front = []
        rectangle = self.rectangles[genotype[0] - 1]
        if self.band_width != rectangle.get_height():
            front.append(FrontLine(self.band_width, rectangle.get_height(), 0))
        front.append(FrontLine(rectangle.get_height(), 0, rectangle.get_width()))
        front.sort(key=lambda n: n.x)

        for gene in genotype[1:]:
            rectangle = self.rectangles[gene - 1]
            for i in range(len(front)):
                if front[i].left_y - front[i].right_y > rectangle.get_height():  # fits on the line
                    front[i].right_y += rectangle.get_height()
                    front.append(FrontLine(front[i].right_y, front[i].right_y - rectangle.get_height(),
                                      front[i].x + rectangle.get_width()))
                    break

                elif (front[i].left_y - front[i].right_y) == rectangle.get_height():  # fits on the line (same height)
                    front[i].x += rectangle.get_width()
                    break

                elif i == (len(front) - 1):  # top line, doesn't fit on it
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
                            newX = front[i].x + rectangle.get_width()
                            newHeight = front[i].right_y + rectangle.get_height()
                            front = list(filter(lambda n: n.left_y > newHeight or n.left_y <= front[i].right_y, front))
                            front.append(FrontLine(newHeight, newHeight - rectangle.get_height(), newX))

                            if newHeight != self.band_width:
                                for j in range(len(front)):
                                    if (front[j].right_y < rectangle.get_height()):
                                        front[j].right_y = rectangle.height
                                        break
                            break
            front.sort(key=lambda n: n.x)

        LineLength = front[-1].x
        FreeArea = self.band_width * LineLength - self.filled_area
        return LineLength, FreeArea

    def fitness(self, genotype):
        length, free_area = self.decode(genotype)

        return length + free_area * self.free_area_dim


fit = Fitness([Rect(5, 6), Rect(2, 2), Rect(6, 6), Rect(1, 2), Rect(3, 3), Rect(2, 10)], filled_area=101, free_dim=100,
              band_width=10)
print(fit([6, 3, 5, 2, 4, 1]))