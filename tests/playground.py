import pandas as pd

# from config import *
from src import magicroot as mr

# print(db.tables.list)


def get_methods_not_dunder(cls):
    return [
        method
        for method in dir(cls) if method.startswith('__') is False
    ]




print('------------- start')


@mr.dynamicclass
class SomeClass:
    var = 0


print('------------- declared class')

x = SomeClass()


@SomeClass.add_method
def some_default_method():
    print('default method')


print('------------- declared default method')

y = SomeClass()

print('------------- initialized instance')


print(get_methods_not_dunder(SomeClass))
print(get_methods_not_dunder(y))
print(get_methods_not_dunder(x))


print('----------------------------------------------')


"""
class SomeClass:
    list = []
    var = 0

    def __init__(self):
        for method in self.list:
            self.__setattr__(method.__name__, method)

    @staticmethod
    def set_default_method(method):
        SomeClass.list.append(method)




class SomeMetaClass:
    __default_method_list = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for method in cls.__default_method_list:
            cls.__setattr__(cls, method.__name__, method)

    @staticmethod
    def set_default_method(method):
        SomeMetaClass.__default_method_list.append(method)

"""

