import pandas as pd
import numpy as np
import os


class Database:
    """
    Database object is used to handle different databases read from diverse type of sources
    """
    def __init__(self, path, sources=None, tables_folder='01 Tabelas', analysis_folder='02 Análises', csv_delimiter=';',
                 csv_decimal=','):
        """
        Creates a Database object
        :param path: Location to save analysis, intermediary tables and fast access tables
        :param sources: Dictionary with all the inputs to be considered in the DataFrame
        :param tables_folder: Name of the folder where the tables will be stored
        :param analysis_folder: Name of the folder where the analysis will be stored
        :param csv_delimiter: Delimiter to be used in .csv outputs
        :param csv_decimal: Decimal character to be used in .csv outputs
        """
        self.__path = path

        self.__create_dir(self.__path, tables_folder)
        self.__create_dir(self.__path, analysis_folder)

        self.__tables_folder = tables_folder
        self.__analysis_folder = analysis_folder
        self.__csv_delimiter = csv_delimiter
        self.__csv_decimal = csv_decimal

        self.config = sources
        self.tables = {}
        self.__reports = {}

    def __getitem__(self, item):
        return self.tables[item]

    def __setitem__(self, key, value):
        self.tables[key] = self.Table(key, df=value)

    def load(self, table_name):
        self.tables[table_name] = self.Table(table_name, self.lib_path)
        return self[table_name]

    def unload(self, table_name):
        df = self[table_name]
        del self.tables[table_name]
        return df

    def create_fast_access_library(self, tables=None):
        """
        Creates copies of the tables in a binary format for fast access
        :return: None
        """
        for table in self.config:
            if tables is None or table in tables:
                df = pd.read_csv(**self.config[table])
                self.save_table(df, table)

    @staticmethod
    def __create_dir(path, name):
        if name not in os.listdir(path):
            os.mkdir(os.path.join(path, name))

    def save_table(self, df, name):
        df.to_feather(os.path.join(self.lib_path, name + '.ftr'))

    def save_analysis(self, df, table_name, analysis_name, cap_rows=100000, **kwargs):
        self.__create_dir(self.analysis_path, table_name)
        df.head(cap_rows).to_csv(
            os.path.join(self.analysis_path, table_name, analysis_name + '.csv'),
            sep=self.__csv_delimiter,
            decimal=self.__csv_decimal,
            **kwargs
        )

    def __check_if_report_exists(self):
        pass

    def __report(self, table_name, analysis_name, n_rows):
        pass

    @property
    def lib_path(self):
        return os.path.join(self.__path, self.__tables_folder)

    @property
    def analysis_path(self):
        return os.path.join(self.__path, self.__analysis_folder)

    @staticmethod
    def percentile(n):
        def percentile_(x):
            return np.percentile(x, n)

        percentile_.__name__ = 'percentile_%s' % n
        return percentile_

    class Table(pd.DataFrame):
        def __init__(self, name, path=None, df=None, **kwargs):
            if path is not None:
                df = pd.read_feather(os.path.join(path, name + '.ftr'))

            super().__init__(df, **kwargs)
            self.name = name
            # self.data = pd.read_feather(os.path.join(path, name + '.ftr'), **kwargs)

        def run_check_nulls(self):
            return self[self.isnull().any(axis=1)]

        def advanced_describe(self, by, compute_map):
            """
            This function creates a Dataframe with aggregator functions grouped by the given columns
            Similarly to the method pandas.DataFrame.describe()
            :param by: list of columns to group the dataframe
            :param compute_map: Two dimensional list with the columns and respective functions
            Each element of the list should have exactly two elements, the first being a list of columns and the
            second being a list of functions.
            The columns should appear only once in the compute_map
            Example:
            [
                [[column_1, column_2], [function_1]],
                [[column_1], [function_1, function_2]
            ]
            :return: a Dataframe with the results
            """
            return self.loc[
                :, [column for n in compute_map for column in n[0]] + by
            ].groupby(by).agg({column: n[1] for n in compute_map for column in n[0]})
