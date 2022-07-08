def make_kernel(mutator_func=None, recomb_func=None, pop_func=None, parent_func=None):
    return Kernel(mutator_func, recomb_func, pop_func, parent_func)


class Kernel:
    def __init__(self, mutator=None, recombinator=None, pop_selector=None, parent_selector=None):

        self.__mutator = mutator
        self.__recombinator = recombinator
        self.__pop_selector = pop_selector
        self.__parent_selector = parent_selector

    def mutation(self, *args, **kwargs):
        if self.__mutator:
            return self.__mutator(*args, **kwargs)

    def recombination(self, *args, **kwargs):
        if self.__recombinator:
            return self.__recombinator(*args, **kwargs)

    def pop_selection(self, *args, **kwargs):
        if self.__pop_selector:
            return self.__pop_selector(*args, **kwargs)

    def parent_selection(self, *args, **kwargs):
        if self.__parent_selector:
            return self.__parent_selector(*args, **kwargs)
