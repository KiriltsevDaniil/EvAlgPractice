from evpy.commands.genetic_operators.wrappers.decorators.command_factory import CommandFactory


class Kernel:
    def __init__(self, mutator=None, recombinator=None, pop_selector=None, parent_selector=None):

        self.__mutator = mutator
        self.__recombinator = recombinator
        self.__pop_selector = pop_selector
        self.__parent_selector = parent_selector

    # (!!!) TO_DO: implement positional and non-positional argument input handling in the same function
    # for now it's only positional for Kernel. Command has a somewhat working prototype,
    # but it probably needs adjustments

    def mutation(self, *args, **kwargs):
        if self.__mutator:
            return self.__mutator(*args)

    def recombination(self, *args, **kwargs):
        if self.__recombinator:
            return self.__recombinator(*args)

    def pop_selection(self, *args, **kwargs):
        if self.__pop_selector:
            return self.__pop_selector(*args)

    def parent_selection(self, *args, **kwargs):
        if self.__parent_selector:
            return self.__parent_selector(*args)
