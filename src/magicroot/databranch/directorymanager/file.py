from .parcers import *
from ...fileleaf import extensions
import logging

log = logging.getLogger('MagicRoot.databranch.directorymanager.file')


class File:
    def __init__(self, path):
        log.debug(f'Creating new file object \'{path}\'')
        self.path = path

    def __str__(self):
        return 'gotta you'

    def __repr__(self):
        return self.__str__()

    def read(self, *args, **kwargs):
        log.debug(f'Reading \'{self.path}\'')
        return self._select_parser().read(*args, **kwargs)

    def save(self, obj, *args, **kwargs):
        log.debug(f'Saving \'{self.path}\'')
        self._select_parser().save(obj, *args, **kwargs)

    def peak(self):
        extension = extensions.get(self.path)
        if extension == '.csv':
            return CSV(self.path).peak(sep=';')
        if extension == '.sas7bdat':
            return SAS(self.path).peak()

    def _select_parser(self):
        log.debug(f'Selecting parcer for \'{self.path}\'')
        extension = extensions.get(self.path)
        if extension == '.json':
            log.debug(f'Selected \'.json\'')
            return JSON(self.path)
        if extension == '.csv':
            log.debug(f'Selected \'.csv\'')
            return CSV(self.path)
        if extension == '.sas7bdat':
            log.debug(f'Selected \'.sas7bdat\'')
            return SAS(self.path)

