from random import uniform
from evpy.commands.genetic_operators.wrappers.command import Command


@Command
def intermediate_recombination(parent1, parent2, n_children=2, d=.25):
    assert d >= 0, "d must be positive or 0"
    masks = [[uniform(-d, 1 + d) for x in parent1] for i in range(n_children)]
    children = []
    for mask in masks:
        child = []
        for i in range(mask):
            child.append(parent1[i] + mask[i]*(parent2[i]-parent1[i]))
        children.append(child)
    parents = [parent1, parent2]
    return parents, children


@Command
def linear_recombination(parent1, parent2, n_children=2, d=.25):
    assert d >= 0, "d must be positive or 0"
    alphas = [uniform(-d, 1 + d) for i in range(n_children)]
    children = []
    for alpha in alphas:
        child = []
        for i in range(parent1):
            child.append(parent1[i] + alpha*(parent2[i]-parent1[i]))
        children.append(child)
    parents = [parent1, parent2]
    return parents, children
