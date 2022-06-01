import os
import re
import getpass
from fuzzywuzzy import process
import ntpath
# from .file import File
from ..beta.fileleaf import extensions
import subprocess
import logging

log = logging.getLogger('MagicRoot.databranch.os.navigator')

class PathNotFound(FileNotFoundError):
    pass


class SubPath:
    def __init__(self, path):
        self.path = path

    @property
    def components(self):
        return self.path.split('\\')

    def __len__(self):
        return self.components.__len__()

    @property
    def root(self):
        return self.components[0]

    @property
    def tail(self):
        return self.components[-1]

    @property
    def name(self):
        return self.tail

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
        # else:
        #     str = f'{str}\n\t{File(self.path).peak()}'

        log.debug(f'Successfully graphical representation of Path')
        return str

    @property
    def files(self):
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    @property
    def directories(self):
        return [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]

    @property
    def contents(self):
        return os.listdir(self.path)

    @property
    def without_user(self):
        _, path = self._split_on_user()
        return path

    @property
    def extension(self):
        return extensions.get(self.path)

    def files_with(self, extension):
        return [file for file in self.files if Path(file).extension == extension]

    def _split_on_user(self):
        log.debug(f'Splitting {self.path} on user: {self.user}')
        return re.split(self.user, self.path)

    def isdir(self):
        return os.path.isdir(self.path)

    def isfile(self):
        return os.path.isfile(self.path)

    def split(self):
        base_path, tail = ntpath.split(self.path)
        tail = tail or ntpath.basename(self.path)
        file_name, extension = os.path.splitext(tail)
        return base_path, file_name, extension

    def change(self, extension):
        base_path, file_name, _ = self.split()
        self.path = os.path.join(base_path, file_name + extension)
        return self

    @classmethod
    def home(cls):
        return Path(os.path.expanduser('~'))


class Navigator(Path):
    """
    This class will save the definitions/permissions of each folder
    """
    def __init__(self, path):
        if len(path) > 256:
            msg = f'The path provided is too long ({len(path)}>256) ' \
                  f'try os.path.exists(path) or os.path.isfile(path) \n path: {path}'
            log.error(msg)
            raise PathNotFound(msg)
        """
        if not (os.path.exists(path) or os.path.isfile(path)):
            msg = f'The path provided to Navigator is not a valid path, ' \
                  f'try os.path.exists(path) or os.path.isfile(path) \npath: \'{path}\' '
            log.error(msg)
            log.debug(f'{os.path.isfile(path)} {os.path.exists(path)}')
            raise PathNotFound(msg) 
        
        """

        super().__init__(path)

    def __getitem__(self, key):
        return self.search(key)

    def search(self, key, on_home=False):
        log.debug(f'Searching \'{self.path}\' for \'{key}\'')
        key = SubPath(key)
        contents = Path.home().contents if on_home else self.contents
        matches = process.extract(key.root, contents)
        log.debug(f'Searched \'{self.path}\' for \'{key.root}\' and found {matches.__str__()}')
        match_path = os.path.join(self.path, matches[0][0])
        folder = Navigator(match_path)
        if len(key) > 1:
            log.debug(f'Will continue search algoritm: Since \'{key}\' has lenght {len(key)}')
            return folder.search(key.without_root)
        log.debug(f'Concluded search algoritm: Since \'{key}\' has lenght {len(key)}')
        return folder

    def open(self):
        path = os.path.join(self.path, self.contents[0])
        subprocess.Popen(r'explorer /select,' + path)

    @classmethod
    def home(cls):
        return Navigator(os.path.expanduser('~'))



