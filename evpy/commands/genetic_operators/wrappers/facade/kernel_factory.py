from evpy.commands.genetic_operators.wrappers.facade.kernel import make_kernel
from evpy.commands.genetic_operators.wrappers.decorators.command_factory import CommandFactory


class KernelFactory:
    def __init__(self, factory_func=make_kernel):

        self.builder = factory_func         # The factory function for Kernel
        self.supplier = CommandFactory()    # The factory function for Commands

    def __build_part(self, command):

        if command:
            return self.supplier.build_command(command)
        else:
            return None

    def build_kernel(self, mutator=None, recombinator=None, pop_selector=None, parent_selector=None):

        _mutator = self.__build_part(mutator)
        _recombinator = self.__build_part(recombinator)
        _pop_selector = self.__build_part(pop_selector)
        _parent_selector = self.__build_part(parent_selector)

        return self.builder(_mutator, _recombinator, _pop_selector, _parent_selector)