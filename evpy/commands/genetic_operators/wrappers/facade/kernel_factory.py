from evpy.commands.genetic_operators.wrappers.facade.kernel import make_kernel
from evpy.commands.genetic_operators.wrappers.decorators.command_list import CommandList
from evpy.commands.genetic_operators.wrappers.decorators.command_factory import CommandFactory


class KernelFactory:
    def __init__(self, factory_func=make_kernel, command_list=None):

        if not command_list:
            self.__commands = CommandList()
        else:
            self.__commands = command_list

        self.builder = factory_func         # The factory function for Kernel
        self.supplier = CommandFactory()    # The factory function for Commands

    def __build_part(self, command_name: str):

        if command_name:
            return self.supplier.build_command(self.__commands.get_command(command_name))
        else:
            return None

    def build_kernel(self, mutator="", recombinator="", pop_selector="", parent_selector=""):

        _mutator = self.__build_part(mutator)
        _recombinator = self.__build_part(recombinator)
        _pop_selector = self.__build_part(pop_selector)
        _parent_selector = self.__build_part(parent_selector)

        return self.builder(_mutator, _recombinator, _pop_selector, _parent_selector)


kerr_factory = KernelFactory()
kerr = KernelFactory.build_kernel(kerr_factory, "point_mutation", "double_point_crossover", "bolzman_selection",
                                  "inbreeding")
print(kerr.mutation([1, 0, 0, 0, 0]))
