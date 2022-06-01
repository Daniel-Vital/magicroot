from openpyxl import load_workbook
import pandas as pd
from .parcer_base import Parser, JSON
import logging
import shutil

log = logging.getLogger('MagicRoot.databranch.os.parcers')


class CSV(Parser):
    extension = 'csv'

    def read(self, *args, **kwargs):
        return pd.read_csv(filepath_or_buffer=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        obj.to_csv(path_or_buf=self.path, *args, **self.save_settings(**kwargs))

    def peak(self, *args, **kwargs):
        return self.read(nrows=5, *args, **kwargs).__repr__()


class SAS(Parser):
    extension = 'sas7bdat'

    def read(self, *args, **kwargs):
        return pd.read_sas(filepath_or_buffer=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        raise NotImplementedError('It is not possible to save sas files')

    def peak(self, *args, **kwargs):
        return self.read(encoding='latin-1', *args, **kwargs).__repr__()


class Excel(Parser):
    extension = 'xlsx'

    def read(self, *args, **kwargs):
        return pd.read_excel(io=self.path, *args, **self.read_settings(**kwargs))

    def save(self, obj, *args, **kwargs):
        """
        book = load_workbook(self.path)
        writer = pd.ExcelWriter(self.path, engine='openpyxl')
        writer.book = book

        ## ExcelWriter for some reason uses writer.sheets to access the sheet.
        ## If you leave it empty it will not know that sheet Main is already there
        ## and will create a new sheet.

        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

        obj.to_excel(writer, *args, **kwargs)

        writer.save()
        """
        raise NotImplementedError('It is not possible to save excel files')

    def peak(self, *args, **kwargs):
        return self.read(encoding='latin-1', *args, **kwargs).__repr__()


class Text(Parser):
    extension = 'txt'

    def read(self, *args, **kwargs):
        return open(self.path, *args, **kwargs)

    def save(self, obj, *args, **kwargs):
        """
        if obj is not None:
            self.read().write(obj)
        """
        try:
            shutil.copyfile(obj.path, self.path)
        except shutil.SameFileError:
            pass
        # raise NotImplementedError('To save to text files read with \'w\'')

    def peak(self, *args, **kwargs):
        return self.read(encoding='latin-1', *args, **kwargs).__repr__()


DEFINED_PARCERS = [CSV, SAS, Excel, Text]
