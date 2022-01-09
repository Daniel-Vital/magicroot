import os

import pandas as pd

from ... import fileleaf as fl


class DatabaseSources:
    """
    This Class is used to handle all the data sources and retrieve the applicable data
    It keeps track of all sources and handles the fast library functionality
    """
    __default_supported_extensions = {
        '.csv': {
            'path': 'filepath_or_buffer',
            'function': pd.read_csv
        },
        '.ftr': {
            'path': 'path',
            'function': pd.read_feather
        }
    }

    def __init__(
            self, supported_extensions=None, folders=None, default_configs=None,
    ):
        """
        In initialization every piece of data is saved in the appropriate place
        :param supported_extensions: This class is build around being able to read data from different sources
        into dataframes, this input defines the supported formats and respective treatments
        It is a dicionary with a 'function' to read the data, and a named parameter 'path' to specify the path
        Example:
        >>> supported_extensions = {
        >>>     '.csv': {
        >>>         'path': 'filepath_or_buffer',
        >>>         'function': pd.read_csv
        >>>     },
        >>>     '.ftr': {
        >>>         'path': 'path',
        >>>         'function': pd.read_feather
        >>>     }
        >>>}
        :param folders: dicionary of reference names and folders (paths) to be considered as sources
        Example:
        >>> folder = {
        >>>     'important sources': r'C:/Users/some_user/some_sources'
        >>>     'other sources': r'C:/Users/some_user/other_sources'
        >>>}
        :param default_configs: defines the default configs for each supported extension
        """
        self.supported_extensions = supported_extensions or self.__default_supported_extensions
        self.folders = folders
        self.default_configs = {**{extension: {} for extension in self.supported_extensions}, **default_configs}

    @property
    def list(self):
        tables = {
            'database_ref': [], 'name': [], 'extension': [],
            'size_MB': [], 'in_fast_lib': [], 'folder': [], 'specific_configs': []
        }

        tables = self.__load_folders(tables)

        df_tables = pd.DataFrame(tables)

        df_tables = self.__mark_in_fast_lib(df_tables)
        df_tables = self.__mark_database_ref(df_tables)

        return df_tables

    def __load_folders(self, tables):
        for folder_name in self.folders:
            dir = self.folders[folder_name]
            for file in os.listdir(dir):
                path = os.path.join(dir, file)
                _, name, extension = fl.split_path(path)
                if extension in self.supported_extensions:
                    tables['database_ref'].append('-')
                    tables['name'].append(name)
                    tables['extension'].append(extension)
                    tables['size_MB'].append(os.path.getsize(path) / 1000000)
                    tables['in_fast_lib'].append(False)
                    tables['folder'].append(folder_name)
                    tables['specific_configs'].append({})
        return tables

    @staticmethod
    def __mark_in_fast_lib(df):
        return df

    @staticmethod
    def __mark_database_ref(df):
        df['database_ref'] = df['name']
        df['n'] = df.index + 1
        df = df.set_index('database_ref')
        return df

    def get_path(self, database_ref):
        folder_name = self.list.loc[database_ref, 'folder']
        folder = self.folders[folder_name]
        name = self.list.loc[database_ref, 'name']
        extension = self.list.loc[database_ref, 'extension']
        return os.path.join(folder, name + extension)

    def get_config(self, database_ref):
        extension = self.list.loc[database_ref, 'extension']
        specific_configs = self.list.loc[database_ref, 'specific_configs']
        return {
            **self.default_configs[extension],
            **specific_configs,
            self.supported_extensions[extension]['path']: self.get_path(database_ref)
        }

    def get_dataframe(self, database_ref):
        extension = self.list.loc[database_ref, 'extension']
        return self.supported_extensions[extension]['function'](
            **self.get_config(database_ref)
        )




