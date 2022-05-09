from dataclasses import dataclass
import os
import shutil
import re
import getpass
import datetime as dt
import pandas as pd
from fuzzywuzzy import process
import subprocess
import datetime
from .navigator import Navigator
import logging

log = logging.getLogger('MagicRoot.databranch.directorymanager.folder')


class Folder(Navigator):
    logger = None

    def __init__(self, path):
        super().__init__(path)

    def log(self, msg=None):
        if Folder.logger is None:
            self._new('.dbLogs')
            logger = logging.getLogger('MagicRoot.databranch.directorymanager.folder.folder_manipulation')
            date_str = str(datetime.datetime.now()).replace('.', '').replace(':', '-')
            log_file = os.path.join(self.path, '.dbLogs', date_str + ' - log.log')
            hand = logging.FileHandler(log_file)
            hand.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
            hand.setFormatter(formatter)

            class NoParsingFilter(logging.Filter):
                def filter(self, record):
                    return record.name == 'MagicRoot.databranch.directorymanager.folder.folder_manipulation'

            hand.addFilter(NoParsingFilter())
            logger.setLevel(logging.DEBUG)
            logger.addHandler(hand)
            Folder.logger = logger

        Folder.logger.debug(msg)

    def new(self, name):
        self.log(f'Creating new folder \'{name}\'')
        self._new(name)
        self.log(f'Successfully created new folder \'{name}\'')

    def _new(self, name):
        new_folder = os.path.join(self.path, name)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

    def remove(self, name):
        self.log(f'Removing folder \'{name}\'')
        folder = os.path.join(self.path, name)
        if os.path.exists(folder):
            shutil.rmtree(folder)
        self.log(f'Successfully removed folder \'{name}\'')

    def search(self, *args, **kwargs):
        return Folder(super().search(*args, **kwargs).path)

    def get(self, file):
        pass


home = Folder(os.path.expanduser('~'))