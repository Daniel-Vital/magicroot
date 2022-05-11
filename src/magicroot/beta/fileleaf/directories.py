import os


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


