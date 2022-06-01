import os
import shutil
from ..beta import fileleaf as fl
import zipfile
import ntpath
import datetime
from .navigator import Navigator
from .file import File
import logging

log = logging.getLogger('MagicRoot.databranch.os.folder')


class Folder(Navigator):
    logger = None

    def __init__(self, path):
        super().__init__(path)

    def log(self, msg=None):
        if Folder.logger is None:
            self._new('.dbLogs')
            logger = logging.getLogger('MagicRoot.databranch.os.folder.folder_manipulation')
            date_str = str(datetime.datetime.now()).replace('.', '').replace(':', '-')
            log_file = os.path.join(self.path, '.dbLogs', date_str + ' - log.log')
            hand = logging.FileHandler(log_file)
            hand.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
            hand.setFormatter(formatter)

            class NoParsingFilter(logging.Filter):
                def filter(self, record):
                    return record.name == 'MagicRoot.databranch.os.folder.folder_manipulation'

            hand.addFilter(NoParsingFilter())
            logger.setLevel(logging.DEBUG)
            logger.addHandler(hand)
            Folder.logger = logger

        Folder.logger.debug(msg)

    def new(self, folder=None, file=None, with_obj=None):
        if folder is not None:
            self.new_folder(folder)
            return Folder(os.path.join(self.path, folder))
        if file is not None:
            self.new_file(file, with_obj)

    def new_file(self, name, obj, *args, **kwargs):
        self.log(f'Creating new file \'{name}\'')
        new_file = os.path.join(self.path, name)
        File(new_file).save(obj, *args, **kwargs)
        self.log(f'Successfully created new file \'{name}\'')

    def new_folder(self, name):
        self.log(f'Creating new folder \'{name}\'')
        self._new(name)
        self.log(f'Successfully created new folder \'{name}\'')
        return Folder(os.path.join(self.path, name))

    def _new(self, name):
        new_folder = os.path.join(self.path, name)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

    def clear(self):
        for obj in self.contents:
            self.remove(obj)

    def remove(self, name):
        self.log(f'Removing \'{name}\'')
        folder = os.path.join(self.path, name)
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        if os.path.isfile(folder):
            os.remove(folder)
        self.log(f'Successfully removed \'{name}\'')

    def search(self, *args, **kwargs):
        return Folder(super().search(*args, **kwargs).path)

    def get(self, file, *args, **kwargs):
        log.debug(f'Retriving \'{file}\' from \'{self.path}\'')
        file_path = os.path.join(self.search(file).path)
        return File(file_path).read(*args, **kwargs)

    def copy(self, to, objs=None, with_new_extension=None):
        objs = objs if objs is not None else self.files
        objs = objs if isinstance(objs, list) else [objs]
        for obj in objs:
            obj = File(self.search(obj).path)
            file_name = obj.tail
            if with_new_extension:
                file_name = File(obj.path).change(extension=with_new_extension).tail
            to.new_file(file_name, obj)

    def move(self, to, objs=None, with_new_extension=None):
        objs = objs if objs is not None else self.files
        objs = objs if isinstance(objs, list) else [objs]
        for obj in objs:
            obj = File(self.search(obj).path)
            file_name = obj.tail
            file_name_new = file_name
            if with_new_extension:
                file_name_new = File(obj.path).change(extension=with_new_extension).tail
            to.new_file(file_name_new, obj)
            self.remove(file_name)

    def unzip(self, to=None, objs=None):
        """
        Unzips a file (.zip) to the given folder
        :param to: folder to which to unzip the files
        :param objs:
        :return: None
        """
        objs = objs if objs is not None else self.files_with(extension='.zip')
        print(objs)
        objs = objs if isinstance(objs, list) else [objs]
        to = to if to is not None else self

        for zip in objs:
            zip_path = os.path.join(self.path, zip)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(to.path)

    def groupby(self, file_name=None):
        """
        Group files in subfolder using a mapping function
        :return:
        """
        grouping_func = file_name
        for file_name in self.files:
            groups = grouping_func(file_name)
            for group in groups:
                group_folder = self.new_folder(group)
                self.move(to=group_folder, objs=file_name)

    @property
    def folders(self):
        return [Folder(os.path.join(self.path, f)) for f in self.directories]


home = Folder(os.path.expanduser('~'))
