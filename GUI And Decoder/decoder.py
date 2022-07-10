class Line:
    def __init__(self, left, right, x):
        self.left = left
        self.right = right
        self.x = x

    def __lt__(self, other):
             return self.x < other.x

class Rect:
    def __init__(self, width, height):
        self.height = height
        self.width = width


def decode(genotype, rectangles, RectArea, LineWidth):
    front = []
    rect = rectangles[genotype[0] - 1]
    if (LineWidth != rect.height):
        front.append(Line(LineWidth, rect.height, 0))
    front.append(Line(rect.height, 0, rect.width))
    front.sort()

    for gen in genotype[1:]:
        print(f"gen: {gen}")
        rect = rectangles[gen - 1]
        print(f"rect: {rect.width}, {rect.height}")
        frontLength = len(front)
        for i in range(frontLength):
            print(f"{i}: left={front[i].left}, right={front[i].right}, x={front[i].x}")
            if (front[i].left - front[i].right) > rect.height: # fits on the line
                print(f"fits on the line")
                newRight = front[i].right + rect.height
                front.append(Line(newRight, front[i].right, front[i].x + rect.width))
                front[i].right = newRight
                break
            elif (front[i].left - front[i].right) == rect.height: # fits on the line (same height)
                print(f"fits on the line (same height)")
                front[i].x += rect.width
                break
            elif i == (frontLength - 1): # top line, doesn't fit on it
                print(f"top line, doesn't fit on it")
                if front[i].left > rect.height:
                    front[i].right = rect.height
                newX = front[i].x + rect.width
                front = list(filter(lambda n: n.left > rect.height, front))
                front.append(Line(rect.height, 0, newX))
                if rect.height != LineWidth:
                    for j in range(len(front)):
                        if (front[j].right < rect.height):
                            front[j].right = rect.height
                            break
                break
            else: # doesn't fit on the line
                print(f"doesn't fit on the line")
                collision = False
                rightBorder = front[i].right + rect.height
                if rightBorder <= LineWidth:
                    for j in range(i+1, frontLength): # check top lines for collision
                        if (front[j].right < rightBorder and front[j].right >= front[i].left):
                            print(f"collision {j}: left={front[j].left}, right={front[j].right}, x={front[j].x}")
                            collision = True
                            break
                    if not collision: # no collision, cover by 'shadow'
                        print(f"no collision")
                        newX = front[i].x + rect.width
                        newHeight = front[i].right + rect.height
                        front = list(filter(lambda n: n.left > newHeight or n.left <= front[i].right, front))
                        front.append(Line(newHeight, newHeight - rect.height, newX))
                        if newHeight != LineWidth:
                            for j in range(len(front)):
                                if (front[j].right < rect.height):
                                    front[j].right = rect.height
                                    break
                        break
        front.sort()
        print()

    LineLength = front[-1].x
    FreeArea = LineWidth * LineLength - RectArea
    print('LineLength: ', LineLength, '\nFreeArea: ', FreeArea)
    return LineLength, FreeArea


if __name__ == "__main__":
    LineWidth = 10
    MaxLineLength = 0
    RectArea = 0
    rectangles = [Rect(5, 6), Rect(2, 2), Rect(6, 6), Rect(1, 2), Rect(3, 3), Rect(2, LineWidth)]
    genotype = [6, 3, 5, 2, 4, 1]
    for i in range(len(rectangles)):
        MaxLineLength += rectangles[i].width
        RectArea += rectangles[i].width * rectangles[i].height
    dim = len(str(MaxLineLength))
    FreeAreaDim = 10**(dim)
    LineLength, FreeArea = decode(genotype, rectangles, RectArea, LineWidth)
    fitness = (LineLength + FreeArea * FreeAreaDim)
    print (f"MaxLineLength={MaxLineLength}, dim={dim}, FreeAreaDim={FreeAreaDim}\nfitness={fitness}")

