from .parcers import *
from ..beta.fileleaf import extensions
import logging

log = logging.getLogger('MagicRoot.databranch.os.file')


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
