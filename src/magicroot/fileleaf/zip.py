import zipfile
import ntpath


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

