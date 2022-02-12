import pandas as pd
from .__default_analysis import DefaultAnalysis


class AnalysisBook:
    """
    Picks the default tests and attaches a save function
    Allows new tests to be defined
    """

    def __get__(self, instance, owner):
        print('Accessing AnalysisBook')
        self.table = instance
        self.save_function = instance.save
        return self.get_available_analysis()

    def method_list(self):
        return [
            DefaultAnalysis().__getattribute__(method)
            for method in dir(DefaultAnalysis) if not method.startswith('__')
        ]

    def get_available_analysis(self):

        class AvailableAnalysis:
            def __init__(self, method_list=None, table=None, save_function=None):
                self.table = table
                self.save_function = save_function
                for method in method_list:
                    name = method.__name__
                    func = self.__analysis(method)
                    self.__setattr__(name, func)

            def __call__(self, func):
                func = self.__analysis(func)
                return func()

            def __analysis(self, func):
                """

                :param func:
                :return:
                """

                def wrapper(*args, **kwargs):
                    rv = func(self.table, *args, **kwargs)
                    self.save_function(df=rv, table_name=self.table.name, analysis_name=func.__name__)
                    return rv

                return wrapper

        available_analysis = AvailableAnalysis(self.method_list(), self.table, self.save_function)

        return available_analysis

    def define_analysis(self, func):
        name = func.__name__
        func = self.__analysis(func)
        self.__setattr__(name, func)

    def all(self):
        raise NotImplementedError

    def __analysis(self, func):
        """

        :param func:
        :return:
        """
        def wrapper(*args, **kwargs):
            rv = func(self.table, *args, **kwargs)
            self.save_function(df=rv, table_name=self.table.name, analysis_name=func.__name__)
            return rv
        return wrapper

    def __set_default_analysis(self):
        method_list = [
            DefaultAnalysis().__getattribute__(method)
            for method in dir(DefaultAnalysis) if not method.startswith('__')
        ]

        for method in method_list:
            self.define_analysis(method)

