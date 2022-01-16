import shutil
from .path import *


def change_file_extension(path, new_extension):
    """
    Creates a copy of a file with a different extension
    :param path: complete path to the file (including the file and extension)
    Example:
    >>> r"C:/Users/some_user/Documents/some_file.csv"
    :param new_extension: extension to give the file
    :return: None
    """
    head, file_name, extension = split_path(path)
    shutil.copy2(path, os.path.join(head, file_name + new_extension))

