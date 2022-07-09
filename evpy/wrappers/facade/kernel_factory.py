from evpy.wrappers.facade.kernel import make_kernel
from evpy.wrappers.decorators.command_factory import CommandFactory


class KernelFactory:
    def __init__(self, kernel_builder: callable = None, command_builder: callable = None):

        if kernel_builder is None:
            kernel_builder = make_kernel

        self.builder = kernel_builder         # The factory function for Kernel
        self.supplier = CommandFactory(command_builder)    # The factory function for Commands

    def __build_part(self, command: callable):

        if command:
            return self.supplier.build_command(command)
        else:
            return None

    def build_kernel(self, mutator: callable = None, recombinator: callable = None,
                     pop_selector: callable = None, parent_selector: callable = None):

        _mutator = self.__build_part(mutator)
        _recombinator = self.__build_part(recombinator)
        _pop_selector = self.__build_part(pop_selector)
        _parent_selector = self.__build_part(parent_selector)

        return self.builder(_mutator, _recombinator, _pop_selector, _parent_selector)
