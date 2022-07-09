from evpy.wrappers.decorators.command import make_command


class CommandFactory:
    def __init__(self, command_builder: callable = None):
        if command_builder is None:
            command_builder = make_command

        self.__builder = command_builder

    def build_command(self, func: callable):
        return self.__builder(func)
