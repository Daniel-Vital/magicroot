import pandas as pd
import os
from ... import fileleaf as fl


class Table(pd.DataFrame):
    """
    Extension of pandas Dataframes with the necessary functionalities
    """
    def __init__(self, df=None, path=None, name=None, **kwargs):
        """
        Creates a table from a path or a Dataframe
        :param df: Dataframe from which to build table
        :param path: Path from which to build table
        :param name: Name to give the Table
        :param kwargs: Arguments to be passed to readers (only relevant when path is given)
        """
        if path is not None:
            _, table_name, extension = fl.split_path(path)
            if extension == '.ftr':
                df = pd.read_feather(path, **kwargs)
            if extension == '.csv':
                df = pd.read_feather(path, **kwargs)
            if name is None:
                name = table_name

        super().__init__(df)
        self.name = name

    @property
    def nulls(self):
        """
        Creates Dataframe with all lines with any null value
        :return: DataFrame with all lines with any null value
        """
        return Table(self[self.isnull().any(axis=1)])

    @property
    def all_duplicated(self):
        """
        Creates Dataframe with all lines which are repeated in all rows
        :return: DataFrame with all lines with all repeated rows
        """
        return Table(self.duplicated(keep=False))

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

    def run_basic_analysis(self):
        return {
            self.name: {
                **self.run_nulls_analysis(),
                **self.run_duplicated_analysis(),
                **self.run_duplicated_index_analysis()
            }
        }

    def run_nulls_analysis(self):
        return {'nulls': self.nulls}

    def run_duplicated_analysis(self):
        return {'duplicated entries': self.all_duplicated}

    def run_duplicated_index_analysis(self):
        return {'duplicated index': self[self.index.duplicated()]}
