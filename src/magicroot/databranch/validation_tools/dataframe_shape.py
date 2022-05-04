import numpy as np


def uniformize_columns(*args):
    """
    Created empty columns in the Dataframes, such that all Dataframes provided have the same columns
    :param args:
    :return:
    """
    columns = list({column for df in args for column in df.columns.to_list()})
    for column in columns:
        for df in args:
            if column not in df:
                df[column] = np.nan
    return args

