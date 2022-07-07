from evpy.commands.genetic_operators.wrappers.decorators.command_factory import CommandFactory


class Kernel:
    def __init__(self, mutator=None, recombinator=None, pop_selector=None, parent_selector=None, random_choice=False):

        builder = CommandFactory()

        if not random_choice:
            if not mutator:
                self.__mutator = None
            else:
                self.__mutator = builder.build_command("mutation", mutator)

            if not recombinator:
                self.__recombinator = None
            else:
                self.__recombinator = builder.build_command("recombination", recombinator)

            if not pop_selector:
                self.__pop_selector = None
            else:
                self.__pop_selector = builder.build_command("population_selector", pop_selector)

            if not parent_selector:
                self.__parent_selector = None
            else:
                self.__parent_selector = builder.build_command("parent_selector", parent_selector)

        else:
            self.__mutator = builder.build_command("mutation")
            self.__recombinator = builder.build_command("recombination")
            self.__pop_selector = builder.build_command("population_selector")
            self.__parent_selector = builder.build_command("parent_selector")

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
