import os
import shutil
import ntpath
import zipfile


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


def unzip_file(path, to=None):
    """
    Unzips a file (.zip) to the given folder
    :param path: complete path to the file (including the file and extension)
    Example:
    >>> r"C:/Users/some_user/Documents/some_file.zip"
    :param to: location to extract files to
    :return: None
    """
    if to is None:
        to, _ = ntpath.split(path)

    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(to)


def split_path(path):
    """
    Returns the parts (base_path, file_name, extension) from a path
    :param path: path to evaluate
    Example
    >>> r"C:/Users/some_user/Documents/some_file.zip"
    :return: parts of file
    Example
    base_path
     >>> r"C:/Users/some_user/Documents/"
    file_name
    >>> "some_file"
    extension
    >>> ".zip"
    """
    base_path, tail = ntpath.split(path)
    tail = tail or ntpath.basename(path)
    file_name, extension = os.path.splitext(tail)
    return base_path, file_name, extension


def print_file_head(path, nrows=10):
    """
    Prints the first rows (nrows) of a file (path)
    :param path: file to print
    :param nrows: number rows to print
    :return: None
    """
    with open(path) as file:
        head = [next(file) for _ in range(nrows)]
    print(head)


def create_folders_missing(directory, folder_names):
    """
    Creates a folder in a directory if the folder does not already exist in such directory
    :param directory: directory to search for folder
    :param folder_names: name of the folder
    :return:
    """
    # creates list if single item is given
    folder_names = [folder_names] if type(folder_names) == str else folder_names
    # iterates through folder names
    for folder_name in folder_names:
        if folder_name not in os.listdir(directory):
            os.mkdir(os.path.join(directory, folder_name))


