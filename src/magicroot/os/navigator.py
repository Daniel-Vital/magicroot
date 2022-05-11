import os
import re
import getpass
from fuzzywuzzy import process
from .file import File
import subprocess
import logging

log = logging.getLogger('MagicRoot.databranch.os.navigator')


class SubPath:
    def __init__(self, path):
        self.path = path

    @property
    def components(self):
        log.debug(f'computing components of \'{self.path}\'')
        return self.path.split('\\')

    def __len__(self):
        return self.components.__len__()

    @property
    def root(self):
        return self.components[0]

    @property
    def without_root(self):
        return os.path.join(*self.components[1:])

    @property
    def without_tail(self):
        return os.path.join(*self.components[:-2])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.path


class Path(SubPath):
    user = getpass.getuser()

    def __init__(self, path):
        super().__init__(path)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        log.debug(f'Creating graphical representation of Path')
        sep_1 = '|\t'
        sep_2 = '|-'
        str = ''
        other_path = self.without_user if len(self.without_user) > 0 else self.path
        str = str + other_path
        if self.isdir():
            for file in self.contents:
                str = f'{str}\n\t{sep_2} {file}'
        else:
            str = f'{str}\n\t{File(self.path).peak()}'

        log.debug(f'Successfully graphical representation of Path')
        return str

    @property
    def contents(self):
        return os.listdir(self.path)

    @property
    def without_user(self):
        _, path = self._split_on_user()
        return path

    def _split_on_user(self):
        log.debug(f'Splitting {self.path} on user: {self.user}')
        return re.split(self.user, self.path)

    def isdir(self):
        return os.path.isdir(self.path)

    def isfile(self):
        return os.path.isfile(self.path)

    @classmethod
    def home(cls):
        return Path(os.path.expanduser('~'))


class Navigator(Path):
    """
    This class will save the definitions/permissions of each folder
    """
    def __init__(self, path):
        log.debug(f'Initializing navigator on \'{path}\'')
        if not os.path.exists(path):
            log.debug(f'The path \'{path}\' provided is not valid searching for match')
            path = self.home().search(path).path
        super().__init__(path)
        log.debug(f'Successfully initialized navigator on \'{path}\'')

    def __getitem__(self, key):
        return self.search(key)

    def search(self, key, on_home=False):
        log.debug(f'Searching \'{self.path}\' for \'{key}\'')
        key=SubPath(key)
        contents = Path.home().contents if on_home else self.contents
        matches = process.extract(key.root, contents)
        log.debug(f'Searched \'{self.path}\' for \'{key.root}\' and found {matches.__str__()}')
        match_path = os.path.join(self.path, matches[0][0])
        folder = Navigator(match_path)
        if len(key) > 1:
            return folder.search(key.without_root)
        return folder

    def open(self):
        path = os.path.join(self.path, self.contents[0])
        subprocess.Popen(r'explorer /select,' + path)

    @classmethod
    def home(cls):
        return Navigator(os.path.expanduser('~'))



