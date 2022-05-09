
from ...fileleaf import extensions
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class Parser:
    def __init__(self, path):
        self.path = path

    def read(self, path, *args, **kwargs):
        pass

    def peak(self, path, *args, **kwargs):
        pass

    def save(self, obj, *args, **kwargs):
        pass


class Csv(Parser):
    def read(self, path, *args, **kwargs):
        return pd.read_csv(filepath_or_buffer=path, *args, **kwargs)

    def save(self, obj, *args, **kwargs):
        obj.to_csv(path_or_buf=self.path, *args, **kwargs)

    def peak(self, *args, **kwargs):
        return self.read(path=self.path, nrows=5, *args, **kwargs).__repr__()


class SAS(Parser):
    def read(self, path, *args, **kwargs):
        return pd.read_sas(filepath_or_buffer=path, *args, **kwargs)

    def save(self, obj, *args, **kwargs):
        raise NotImplementedError('It is not possible to save sas files')

    def peak(self, *args, **kwargs):
        return self.read(path=self.path, encoding='latin-1', *args, **kwargs).__repr__()


class File:
    map = {
        '.csv': Csv,
        '.sas7bdat': SAS
    }

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'gotta you'

    def __repr__(self):
        return self.__str__()

    def peak(self):
        extension = extensions.get(self.path)
        if extension == '.csv':
            return Csv(self.path).peak(sep=';')
        if extension == '.sas7bdat':
            return SAS(self.path).peak()

