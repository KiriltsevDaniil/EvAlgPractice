from Problem.rectangle import Rect
#
# def fitness(genotype: list, free_area, rectangles: list, free_area_dim, band_length):


class Model:
    def __init__(self):
        self.band_width = 0     # W
        self.free_area_dim = 0  # разряды площади оставшейся
        self.filled_area = 0
        self.rectangles = []    # rectangles

        self.solver = None

    def solve(self):
        pass
        # genetic algorithm here

    def process_data(self, band_width: int, rects: list):
        self.band_width = band_width
        max_length, rect_area = 0, 0

        for i in range(1, len(rects), 2):
            self.rectangles.append(Rect(rects[i-1], rects[i]))
            max_length += rects[i-1]
            rect_area += rects[i-1] * rects[i]

        self.filled_area = rect_area
        self.free_area_dim = 10 ** len((str(max_length)))
