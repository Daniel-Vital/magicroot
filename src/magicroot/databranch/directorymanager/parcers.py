
import os.path

import pandas as pd
from .parcer_base import Parser, JSON
import logging

log = logging.getLogger('MagicRoot.databranch.directorymanager.parcers')


class CSV(Parser):
    extension = 'csv'

    def read(self, *args, **kwargs):
        return pd.read_csv(filepath_or_buffer=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        obj.to_csv(path_or_buf=self.path, *args, **self.save_settings(**kwargs))

    def peak(self, *args, **kwargs):
        return self.read(nrows=5, *args, **kwargs).__repr__()


class SAS(Parser):
    extension = 'sas7bdat'

    def read(self, *args, **kwargs):
        return pd.read_sas(filepath_or_buffer=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        raise NotImplementedError('It is not possible to save sas files')

    def peak(self, *args, **kwargs):
        return self.read(encoding='latin-1', *args, **kwargs).__repr__()

