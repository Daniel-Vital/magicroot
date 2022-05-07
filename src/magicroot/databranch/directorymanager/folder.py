from dataclasses import dataclass
import os
import re
import getpass
import datetime as dt
import pandas as pd
from fuzzywuzzy import process
import subprocess
import logging

log = logging.getLogger('MagicRoot.Folder')


class NoPermissionError(Exception):
    pass


class DirectoriesManager:
    def __init__(self, base_path, paths):
        self._data = pd.DataFrame()
        self._base = base_path

        for path in paths:
            folder = Folder(path=path)
            self._data = self._data.append(folder.to_dict(), ignore_index=True)

    @property
    def data(self):
        return self._data

    def save(self):
        writing_folder = Folder(self._base)
        writing_folder.readonly = False
        writing_folder.save(self._data, 'list_of_folders')


class Folder:
    """
    This class will save the definitions/permissions of each folder
    """
    def __init__(self, path):
        self.user = getpass.getuser()
        self.os, self.folder = re.split(self.user, path)
        self.readonly = True
        self.overwrite = False
        self.extensions = ['.csv', '.ftr']

    @property
    def path(self):
        return self.os + self.user + self.folder

    @property
    def contents(self):
        return os.listdir(self.path)

    def save(self, df, file_name):
        if self.readonly:
            raise NoPermissionError(f'Readonly Folder {self.folder}')
        name = os.path.join(self.path, file_name + '.csv')
        df.to_csv(path_or_buf=name)

    def to_dict(self):
        return {
            'Date': dt.datetime.now(),
            'Readonly': str(self.readonly),
            'Last_User': self.user,
            'Folder': self.folder,
            'OS': self.os,
            'Extensions': self.extensions
        }

    def to_dataframe(self):
        return pd.DataFrame(self.to_dict())

    def __getitem__(self, key):
        all_inputs = key.split('\\')
        current_input = all_inputs[0]
        match = process.extract(current_input, self.contents)
        log.debug(match.__str__())
        folder = Folder(os.path.join(self.path, match[0][0]))
        if len(all_inputs) > 1:
            return folder[os.path.join(*all_inputs[1:])]
        return folder

    def open(self):
        print(self.path)
        subprocess.Popen(r'explorer /select,' + self.path)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        sep_1 = '│\t'
        sep_2 = '├──'
        str = ''
        str = str + self.folder

        for file in self.contents:
            str = f'{str}\n\t{sep_2} {file}'

        return str


home = Folder(os.path.expanduser('~'))

parser = {
    '.csv': {
        'path': 'filepath_or_buffer',
        'function': pd.read_csv
    }
}


class Parser:
    def read(self, path, *args, **kwargs):
        pass

    def write(self, path, *args, **kwargs):
        pass

    @property
    def extension(self):
        raise NotImplementedError




