import pandas as pd
import numpy as np
import os
import datetime as dt
from .database_structures.__table import Table
from .database_structures.__sources import DatabaseSources as Sources
from .. import fileleaf as fl


class Database:
    """
    Database object is used to handle different databases read from diverse type of sources
    """

    def __init__(self, path, tables_folder='01 Tabelas', analysis_folder='02 Análises', csv_delimiter=';',
                 csv_decimal=',', folders=None, **kwargs):
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

        self.tables = Sources(
            folders={**folders, 'internal lib': self.lib_path},
            fast_access_lib_ref='internal lib',
            **kwargs
        )
        self.loaded_tables = {}
        self.dictionaries = {}
        self.__report = pd.DataFrame({'date': [], 'table_name': [], 'analysis_name': [], 'n_rows': []})

    def __getitem__(self, item):
        if item not in self.loaded_tables:
            self.load(item)
        return self.loaded_tables[item]

    def __setitem__(self, key, value):
        self.loaded_tables[key] = Table(key, df=value)

    def load(self, table_name):
        self.loaded_tables[table_name] = Table(df=self.tables.get_dataframe(table_name), name=table_name)

    def unload(self, table_name):
        df = self[table_name]
        del self.loaded_tables[table_name]
        return df

    def save_to_fast_access_lib(self, tables=None):
        """
        Creates copies of the tables in a binary format for fast access
        :return: None
        """
        tables = [tables] if type(tables) == str else tables
        for table in tables:
            self.save_table(self[table], table)

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
        self.__append_to_report(table_name, analysis_name, len(df))

    def save_analysis_from_dic(self, dic):
        """
        Saves multiple analysis from a dic
        :param dic: dictionary with the analysis
        Example:
        >>> dic = {'some_table_name': {'some_analysis_name': dataframe_with_analysis}}
        :return: None
        """
        for table in dic:
            for analysis in dic[table]:
                self.save_analysis(df=dic[table][analysis], table_name=table, analysis_name=analysis)

    def run_basic_analysis(self, table_name, df=None):
        df = Table(df, name=table_name) if df is not None else self[table_name]
        self.save_analysis_from_dic(df.run_basic_analysis())

    def __append_to_report(self, table_name, analysis_name, n_rows, **kwargs):
        self.__report = self.__report.append(
            {'date': dt.datetime.now(), 'table_name': table_name, 'analysis_name': analysis_name, 'n_rows': n_rows},
            ignore_index=True
        )
        self.save_table(self.__report, 'report')
        self.__report.to_csv(
            os.path.join(self.analysis_path, 'report.csv'),
            sep=self.__csv_delimiter,
            decimal=self.__csv_decimal,
            **kwargs
        )

    def replace_from_dataframe(self, df):
        """
        This function is intended to replace
        :param df:
        :return:
        """
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

    def replace_code_row(self, from_table, with_table, key_columns):
        """
        In many databases to save on space it is common to replace discrete variables with codes, for example
        instead of having
        TABLE A
        car     |   brand
        1           Ferrari
        2           Lamborghini
        3           Tesla
        ...

        it much more memory efficient to have (specially if you have millions of 'Ferrari's in your table)
        TABLE B
        car     |   brand
        1           001
        2           002
        3           003
        ...

        and then have a table with the codes
        TABLE C
        brand   |   Desc_brand
        001         Ferrari
        002         Lamborghini
        003         Tesla
        ...

        However, to analyse tables and construct reports and graphs, specially after grouping the table
        these codes make reading such reports almost impossible, since one must always refer back to
        the dictionary table (TABLE C from example).
        :param from_table: table in which the key_columns will be replaced (TABLE B from example)
        :param with_table: table in from which the description of the key_columns will be read (TABLE C from example)
        :param key_columns: key to read should be given as a dictionary in the example above would be
        {'brand': 'Desc_brand'}
        The keys of the dictionaries represent columns from both tables and are the columns to be replaced in the
        'from_table'.
        The values from the dictionary represent columns from the 'with_table' and are the values than will be in the
        'return'.
        :return: table the full keys (TABLE A from example)
        """
        replace_dicionary = {}
        for column in key_columns:
            replace_dicionary_2 = {}

        return self[from_table].replace(self[with_table][key_columns].to_dic())

    def __create_complete_description(self, from_table, key_columns, prefix='CDesc'):
        """
        Completes the keys descriptions of a dictionary table
        for example transforms a table such as
        TABLE A
        brand   |   model       |   Desc_brand  |   Desc_model
        001         001             Ferrari         812 GTS
        002         001             Lamborghini     Aventador
        003         001             Tesla           Model X
        003         002             Tesla           Model Y
        ...

        into something like
        TABLE B
        brand   |   model       |   Desc_brand  |   Desc_model  |   CDesc_brand         |   CDesc_model
        001         001             Ferrari         812 GTS         Ferrari (001)           812 GTS (001)
        002         001             Lamborghini     Aventador       Lamborghini (002)       Aventador (001)
        003         001             Tesla           Model X         Tesla (003)             Model X (001)
        003         002             Tesla           Model Y         Tesla (003)             Model Y (002)
        ...

        :param from_table: name of table with the keys and descriptions (Table A)
        :param key_columns: dictionary with the columns and descriptions to be treated
        >>> example_key = {'brand': 'Desc_brand', 'model': 'Desc_model'}
        :param prefix: prefix for created columns, default is 'CDesc' for Complete Description
        :return: table with the appropriate descriptions for graphs and reports (Table B)
        """
        df = self[from_table]
        for column in key_columns:
            description_column = key_columns[column]
            new_colum_name = prefix + '_' + column
            df[new_colum_name] = df[description_column] + ' (' + df[column] + ')'

    def __create_replace_dictionary(self, from_table, key):
        """
        Transforms a table into a replacement dictionary
        for example transforms a table such as
        TABLE A
        brand   |   model       |   Desc_brand  |   Desc_model
        001         001             Ferrari         812 GTS
        002         001             Lamborghini     Aventador
        003         001             Tesla           Model X
        003         002             Tesla           Model Y
        ...

        {'brand': 'Desc_brand', 'model': 'Desc_model'}

        into the following dictionary
        {'brand': {'001': 'Ferrari', '002': 'Lamborghini', '003': 'Tesla'}}

        :param from_table:
        :param key:
        :return:
        """
        pass

    def declare_dictionary(self, with_name, from_table, key, description):
        """
        Creates a dicionary to be used to replace a
        :param with_name:
        :param from_table:
        :param key:
        :param description:
        :return:
        """
        pass

    def apply_dictionary(self, with_name, to_table):
        """
        Applies a dictionary to a table in the database
        see description of declare_dictionary
        example:
        >>> db = Database() # dummy database needs arguments
        >>> db.declare_dictionary(
        ...             with_name='myDic', from_table='some_table',
        ...             key='some_column', description='some_column_with_description_of_key')
        >>> db.apply_dictionary(with_name='myDic', to_table='some_other_table')

        :param with_name: name of the dictionary
        :param to_table: name of table to which the dictionary will be applied
        :return:
        """
        self[to_table] = self[to_table].replace(self.dictionaries[with_name])
