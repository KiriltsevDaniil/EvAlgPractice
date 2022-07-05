from random import randint

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

    