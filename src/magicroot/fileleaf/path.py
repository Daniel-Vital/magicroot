import ntpath
import os


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
