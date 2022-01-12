import pandas as pd
from .__default_analysis import DefaultAnalysis


class AnalysisBook:
    def __init__(self):
        self.df = pd.DataFrame()
        self.save_function = lambda df, table_name, analysis_name: 0
        self.__set_default_analysis()

    def set(self, df, save_function):
        self.df = df
        self.save_function = save_function
        return self

    def define_analysis(self, func):
        name = func.__name__
        func = self.analysis(func)
        self.__setattr__(name, func)

    def analysis(self, func):
        """

        :param func:
        :return:
        """
        def wrapper(*args, **kwargs):
            rv = func(self.df, *args, **kwargs)
            self.save_function(df=rv, table_name=self.df.name, analysis_name=func.__name__)
            return rv
        return wrapper

    def __set_default_analysis(self):
        method_list = [
            DefaultAnalysis().__getattribute__(method)
            for method in dir(DefaultAnalysis) if method.startswith('__') is False
        ]

        for method in method_list:
            self.define_analysis(method)


