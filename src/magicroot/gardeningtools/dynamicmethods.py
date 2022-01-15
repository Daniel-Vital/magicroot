
def dynamicclass(cls):
    """
    Decorator to allow creation of dynamic methods in classes
    Example:
    >>> @dynamicclass
    >>> class SomeClass:
    >>>     var = 0

    >>> @SomeClass.add_method
    >>> def some_new_method():
    >>>     print('default method')

    >>> x = SomeClass()
    >>> x.some_new_method()
    :param cls: class in with to allow dynamic methods
    :return: derived class
    """

    class NewCls(cls):
        __default_method_list = []

        def __init__(self, *args, **kwargs):
            for method in self.__default_method_list:
                self.__setattr__(method.__name__, method)
            super().__init__(*args, **kwargs)

        @classmethod
        def add_method(cls, method):
            cls.__default_method_list.append(method)
            return method

    return NewCls
