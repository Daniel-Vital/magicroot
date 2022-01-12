import pandas as pd


class AnalysisBook:
    def __init__(self):
        # self.analysis = {nulls}

        self.df = pd.DataFrame()
        self.save_function = lambda df, table_name, analysis_name: 0

        #for analysis in self.analysis:
        #    self.__setattr__(analysis.__name__, analysis)

    def set(self, df, save_function):
        self.df = df
        self.save_function = save_function
        return self

    def define_analysis(self, func):
        def wrapper(*args, **kwargs):
            rv = func(self.df, *args, **kwargs)
            self.save_function(df=rv, table_name=self.df.name, analysis_name=func.__name__)
            return rv

        self.__setattr__(func.__name__, wrapper)

    @property
    def nulls(self):
        """
        Creates Dataframe with all lines with any null value
        :return: DataFrame with all lines with any null value
        """
        df = self.df[self.df.isnull().any(axis=1)]
        self.save_function(df=df, table_name=self.df.name, analysis_name='nulls')
        return df
