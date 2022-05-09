import os
import json
from ...settings.settings_locator import settings_path as base_settings_path
import pandas as pd
import logging

log = logging.getLogger(__name__)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class Parser:
    extension = None

    def __init__(self, path):
        self.path = path

    def read(self, path, *args, **kwargs):
        pass

    def peak(self, path, *args, **kwargs):
        pass

    def save(self, obj, *args, **kwargs):
        pass

    @classmethod
    def read_settings(cls, **kwargs):
        try:
            return {**cls.load_default_settings()['read'], **kwargs}
        except FileNotFoundError:
            return kwargs

    @classmethod
    def save_settings(cls, **kwargs):
        try:
            return {**cls.load_default_settings()['save'], **kwargs}
        except FileNotFoundError:
            return kwargs

    @classmethod
    def settings_path(cls):
        return os.path.join(base_settings_path, cls.extension + '.json')

    @classmethod
    def set_default_settings(cls, settings):
        log.debug(f'Setting default settings for \'{cls.extension}\'')
        JSON(cls.settings_path()).save(settings)

    @classmethod
    def load_default_settings(cls):
        log.debug(f'Loading default settings for \'{cls.extension}\'')
        return JSON(cls.settings_path()).read()


class JSON(Parser):
    extension = 'json'

    def read(self, *args, **kwargs):
        log.debug(f'Reading .json \'{self.path}\'')
        with open(self.path, 'r') as f:
            return json.load(f)

    def save(self, obj, *args, **kwargs):
        log.debug(f'Saving .json \'{self.path}\'')
        with open(self.path, 'w+') as outfile:
            json.dump(obj, outfile)

    def peak(self, *args, **kwargs):
        log.debug(f'Peaking .json \'{self.path}\'')
        return self.read(*args, **kwargs).__repr__()
