import json
import pandas as pd
from .parcer import Parser
import logging

log = logging.getLogger('MagicRoot.databranch.directorymanager.parcers')


class JSON(Parser):
    extension = '.json'

    def read(self, *args, **kwargs):
        log.debug(f'Reading .json \'{self.path}\'')
        with open(self.path, 'r') as f:
            return json.load(f)

    def save(self, obj, *args, **kwargs):
        log.debug(f'Saving .json \'{self.path}\'')
        with open(self.path, 'w') as outfile:
            json.dump(obj, outfile)

    def peak(self, *args, **kwargs):
        log.debug(f'Peaking .json \'{self.path}\'')
        return self.read(*args, **kwargs).__repr__()


class CSV(Parser):
    extension = '.csv'

    def read(self, *args, **kwargs):
        return pd.read_csv(filepath_or_buffer=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        obj.to_csv(path_or_buf=self.path, *args, **self.save_settings(**kwargs))

    def peak(self, *args, **kwargs):
        return self.read(nrows=5, *args, **kwargs).__repr__()

    @classmethod
    def set_default_settings(cls, settings):
        JSON('src\\magicroot\\settings\\csv.json').save(settings)

    @classmethod
    def load_default_settings(cls):
        return JSON('src\\magicroot\\settings\\csv.json').read()


class SAS(Parser):
    extension = '.sas7bdat'

    def read(self, *args, **kwargs):
        return pd.read_sas(filepath_or_buffer=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        raise NotImplementedError('It is not possible to save sas files')

    def peak(self, *args, **kwargs):
        return self.read(encoding='latin-1', *args, **kwargs).__repr__()

    @classmethod
    def set_default_settings(cls, settings):
        JSON('src\\magicroot\\settings\\sas.json').save(settings)

    @classmethod
    def load_default_settings(cls):
        return JSON('src\\magicroot\\settings\\sas.json').read()

