from evpy.commands.genetic_operators.wrappers.decorators.command import make_command
from evpy.commands.genetic_operators.wrappers.decorators.command_list import CommandList


class CommandFactory:
    def __init__(self, factory_func=make_command, commands=None):

        if not commands:
            commands = CommandList()

        self.__available = commands
        self.__factory = factory_func

    def get_categories(self):
        return self.__available.show_supported()

    def build_command(self, category: str, func=""):
        if func:
            if self.__available.check_category(category) and self.__available.check_function(func):
                return self.__factory(self.__available.get_command(category, func))
        else:
            if self.__available.check_category(category):
                return self.__factory(self.__available.get_command(category))

    def build_custom(self, func):
        return self.__factory(func)
