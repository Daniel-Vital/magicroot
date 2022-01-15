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


def is_csv(path):
    """
    Evaluates if a file is a csv
    :param path: file to evaluate
    :return: True if file is a csv, False otherwise
    """
    if path[-4:] == '.csv':
        return True
    return False


def get_all_csv(path):
    """
    Returns all the csv files from a directory
    :param path: directory to evaluate
    :return: list of all csv files paths
    """
    # Extracting all the contents in the directory corresponding to path
    l_files = os.listdir(path)

    csv_files = []

    for i, file in enumerate(l_files):
        if is_csv(file):
            csv_files.append(file)

    return csv_files
