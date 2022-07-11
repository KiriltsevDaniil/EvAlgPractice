from random import randint, sample


def discrete_recombination(parent1, parent2, n_children=2):
    '''a.k.a. uniform crossover'''
    masks = [[randint(1, 2) for x in parent1] for i in range(n_children)]
    children = []
    for mask in masks:
        child = []
        for i in range(mask):
            child.append(parent1[i]) if mask[i] == 1 else child.append(parent2[i])
        children.append(child)
    parents = [parent1, parent2]
    return parents, children


def discrete_unique(parent1, parent2):
    offspring = [[parent1[0]] + sample(parent1[1:], k= len(parent1) - 1),
    [parent2[0]] + sample(parent2[1:], k= len(parent1) - 1)]
    return [parent1, parent2], offspring