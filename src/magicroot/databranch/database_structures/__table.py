import pandas as pd
import os
from ... import fileleaf as fl
from .__analysis_book import AnalysisBook


class Table(pd.DataFrame):
    """
    Extension of pandas Dataframes with the necessary functionalities
    """
    analyse = AnalysisBook()

    def __init__(self, df=None, path=None, name=None, analysis_book=None, save_function=None, **kwargs):
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
        self.save = save_function

    def set_index(self, *args, **kwargs):
        return Table(name=self.name, df=super(Table, self).set_index(*args, **kwargs))
