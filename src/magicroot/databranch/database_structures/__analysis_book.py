import pandas as pd
from .__default_analysis import DefaultAnalysis


class AnalysisBook:
    def __init__(self, table=None, save_function=None):
        self.table = table
        self.save_function = save_function
        for method in self.method_list():
            name = method.__name__
            func = self.__apply_save_function(method)
            self.__setattr__(name, func)

    def __call__(self, func):
        func = self.__apply_save_function(func)
        return func()

    def __apply_save_function(self, func):
        """
        Applies a save function to all analysis
        :param func: save function to be applied
        :return: original function with the save function applied
        """
        if self.save_function is None:
            return func

        def wrapper(*args, **kwargs):
            rv = func(self.table, *args, **kwargs)
            self.save_function(df=rv, table_name=self.table.name, analysis_name=func.__name__)
            return rv

        return wrapper

    @staticmethod
    def method_list():
        return [
            DefaultAnalysis().__getattribute__(method)
            for method in dir(DefaultAnalysis) if not method.startswith('__')
        ]


class Analyser:
    """
    Picks the default tests and attaches a save function
    Allows new tests to be defined
    """

    def __get__(self, instance, owner):
        return AnalysisBook(instance, instance.save)



