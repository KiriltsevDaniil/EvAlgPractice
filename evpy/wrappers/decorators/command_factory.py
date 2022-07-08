from evpy.wrappers.decorators.command import make_command


class CommandFactory:
    def __init__(self, factory_func=make_command):

        self.__factory = factory_func

    def build_command(self, func):
        return self.__factory(func)
