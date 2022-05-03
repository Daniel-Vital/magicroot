import os
import pandas as pd


def is_sas_table(path):
    """
    Evaluates if a file is a sas table
    :param path: file to evaluate
    :return: True if file is a csv, False otherwise
    """
    if path[-9:] == '.sas7bdat':
        return True
    return False


def get_all_sas_tables(path):
    """
    Returns all the sas tables from a directory
    :param path: directory to evaluate
    :return: list of all sas files paths
    """
    # Extracting all the contents in the directory corresponding to path
    l_files = os.listdir(path)

    sas_files = []

    for i, file in enumerate(l_files):
        if is_sas_table(file):
            sas_files.append(file)

    return sas_files


def copy_to_csv(input_path, output_path=None, **kwargs):
    output_path = output_path if output_path is not None else input_path
    for table in get_all_sas_tables(input_path):
        try:
            print(os.path.join(input_path, table))
            df = pd.read_sas(filepath_or_buffer=os.path.join(input_path, table), format='sas7bdat', encoding='utf-8')

            print(df.head())
            df.to_csv(os.path.join(output_path, table + '.csv'), **kwargs)
        except (ValueError, AttributeError) as e:
            print(e)


