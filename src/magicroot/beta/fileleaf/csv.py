import logging
import os
log = logging.getLogger('CSV_')


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


def has_equal_len_lines(path, delimiter=','):
    """
    Evaluates if a CSV has the same number of entries in each line
    :param path: file to evaluate
    :param delimiter: delimiter to consider in csv
    :return: True if file needs preprocessing, False otherwise
    """
    log.debug('\t\t Evaluating if file has all lines with equal len')
    file = open(path, 'r')

    all_lines_equal_len = True
    differences = []
    previous_line = ''
    for i, line in enumerate(file):
        if i > 0:
            if line.count(delimiter) != previous_line.count(delimiter):
                all_lines_equal_len = False
                differences.append(i+1)
        previous_line = line

    file.close()

    if not all_lines_equal_len:
        log.debug('\t\t found differences in lines {}'.format(differences))
    else:
        log.debug('\t\t No differences found')

    return all_lines_equal_len

