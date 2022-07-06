from random import randint, sample


def single_point_crossover(parent1, parent2):
    point = randint(0, len(parent1)-1)
    children = [parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]]
    parents = [parent1, parent2]
    return parents, children


def double_point_crossover(parent1, parent2):
    tmp1, tmp2 = parent1, parent2
    for i in range(2):
        _, tmps = single_point_crossover(tmp1, tmp2)
        tmp1, tmp2 = tmps
    parents = parent1, parent2
    return parents, tmps


def multi_point_crossover(parent1, parent2, n=3):
    tmp1, tmp2 = parent1, parent2
    for i in range(n):
        _, tmps = single_point_crossover(tmp1, tmp2)
        tmp1, tmp2 = tmps
    parents = parent1, parent2
    return parents, tmps


def shuffler_crossover(parent1, parent2, parent_shuffle_k=5, child_shuffle_k=5):
    for _ in range(parent_shuffle_k):
        point = randint(0, len(parent1) - 1)
        parent1[point], parent2[point] = parent2[point], parent1[point]
    
    parents, children = single_point_crossover(parent1, parent2)

    for _ in range(child_shuffle_k):
        point = randint(0, len(parent1) - 1)
        children[0][point], children[1][point] = children[1][point], children[0][point]

    return parents, children


def single_point_rsc(parent1, parent2):
    '''rsc - reduced surrogate crossover'''
    rs_points = [i for i in range(len(parent1)) if parent1[i] != parent2[i]]
    point = sample(rs_points, k=1) if rs_points else randint(0, len(parent1)-1)
    point = randint(0, len(parent1)-1)
    children = [parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]]
    children.append()
    parents = [parent1, parent2]
    return parents, children
