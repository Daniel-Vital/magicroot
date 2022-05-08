from dataclasses import dataclass
import os
import shutil
import re
import getpass
import datetime as dt
import pandas as pd
from fuzzywuzzy import process
import subprocess
from .navigator import Navigator
import logging

log = logging.getLogger('MagicRoot.databranch.directorymanager.navigator')


class Folder(Navigator):
    def __init__(self, path):
        super().__init__(path)

    def log(self, msg=None):
        self._new('.dbLogs')

    def new(self, name):
        self.log()
        self._new(name)

    def _new(self, name):
        new_folder = os.path.join(self.path, name)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

    def remove(self, name):
        self.log()
        # files: os.remove('file_path')
        # empty folder: os.rmdir('empty_dir_path')
        # remove all: shutil.rmtree('dir_path')
        folder = os.path.join(self.path, name)
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def search(self, *args, **kwargs):
        return Folder(super().search(*args, **kwargs).path)


home = Folder(os.path.expanduser('~'))