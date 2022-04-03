class Stack:
    def __init__(self, name):
        self.__stack_name = name

    @staticmethod
    def create_stack(name):
        return Stack(name)

    @property
    def stack_name(self):
        return self.__stack_name

    @stack_name.setter
    def stack_name(self, value):
        self.__stack_name = value
