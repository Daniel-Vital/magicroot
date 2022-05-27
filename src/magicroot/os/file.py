from .parcers import *
from .navigator import Navigator
from .parcer_base import Parser
from ..beta.fileleaf import extensions
import os
import shutil
import logging

log = logging.getLogger('MagicRoot.databranch.os.file')


class ParcerNotFound(FileNotFoundError):
    pass


class File(Navigator, Parser):
    def __init__(self, path):
        super(File, self).__init__(path)
        log.debug(f'Creating new file object \'{path}\'')
        # self.path = path

    def __str__(self):
        str = f'No parcer was found for extension type \'{self.extension}\'\n {self.path}'
        return str

    def __repr__(self):
        return self.__str__()

    def read(self, *args, **kwargs):
        log.debug(f'Reading \'{self.path}\'')
        try:
            return self._select_parser().read(*args, **kwargs)
        except ParcerNotFound:
            return self

    def save(self, obj, *args, **kwargs):
        log.debug(f'Saving \'{self.path}\'')
        try:
            self._select_parser().save(obj, *args, **kwargs)
        except ParcerNotFound:
            shutil.copyfile(obj.path, self.path)

    def peak(self):
        extension = extensions.get(self.path)
        if extension == '.csv':
            return CSV(self.path).peak()
        if extension == '.sas7bdat':
            return SAS(self.path).peak()

    def _select_parser(self):
        log.debug(f'Selecting parcer for \'{self.path}\'')
        extension = extensions.get(self.path)
        if extension == '.json':
            log.debug(f'Selected \'.json\'')
            return JSON(self.path)
        for Parcer in DEFINED_PARCERS:
            if extension == '.' + Parcer.extension:
                log.debug(f'Selected \'{Parcer.extension}\'')
                return Parcer(self.path)

        raise ParcerNotFound(f'No parcer was found for extension type \'{extension}\'')
