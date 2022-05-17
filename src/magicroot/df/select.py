import numpy as np


def numeric_columns(df, invert=False, remove=None):
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
    if remove:
        columns.remove(remove)
    return columns


def columns_in_list(*args, columns):
    return [column for column in columns for df in args if column in df.columns]
