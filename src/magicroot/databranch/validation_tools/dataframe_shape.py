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


def get_numeric_columns(df, invert=False, remove=None):
    """
    Return a list of the numeric columns of a Dataframe
    :param df:
    :param invert: Modifier to return a list of the non-numeric columns of a Dataframe
    :param remove: Columns to remove from output
    :return:
    """
    if invert:
        columns = df.select_dtypes(exclude=np.number).columns.to_list()
    else:
        columns = df.select_dtypes(include=np.number).columns.to_list()
    columns.remove(remove)
    return columns
