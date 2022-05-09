import json

from ...settings.settings_locator import settings_path
import pandas as pd
import logging

log = logging.getLogger('MagicRoot.databranch.directorymanager.parcer')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class Parser:
    extension = None
    settings_path = settings_path

    def __init__(self, path):
        self.path = path

    def read(self, path, *args, **kwargs):
        pass

    def peak(self, path, *args, **kwargs):
        pass

    def save(self, obj, *args, **kwargs):
        pass

    @classmethod
    def load_default_settings(cls):
        return {}

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

