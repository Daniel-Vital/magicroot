import pandas as pd


def with_func(df, columns, func):
    """
    Tranforms the given columns based on the given function
    :param df: Table to be transformed
    :param columns: columns to be transformed
    :param func: function that receives the dataframe and the name of the column to be formated
    :return:
    """
    columns = columns if columns is not None else df.columns
    for column in columns:
        if column in df.columns:
            df = df.assign(**{column: func(df, column)})
    # return df.assign(**{column: lambda x: func(x, column) for column in columns if column in df.columns})
    return df


def as_date(df, columns=None, *args, **kwargs):
    """
    Tranforms the given columns into european dates in the given table
    :param df: Table to be transformed
    :param columns: columns to be transformed
    :return:
    """
    return with_func(df, columns, lambda x, column: pd.to_datetime(df[column], *args, **kwargs))


def as_set_len_code(df, columns=None):
    """
    Tranforms the given columns into set lenght codes (ex. '001')
    :param df: Table to be transformed
    :param columns: dict
    columns to be transformed as keys, lenght of expected results as values
    :param lenght: columns to be transformed
    :return:
    """
    for column, lenght in columns.items():
        df = with_func(df, [column], lambda x, col: x[col].astype(str).str.zfill(lenght))
    return df


def as_float(df, columns=None):
    """
    Tranforms the given columns into floats
    :param df: Table to be transformed
    :param columns: dict
    columns to be transformed as keys, lenght of expected results as values
    :param lenght: columns to be transformed
    :return:
    """
    for column, lenght in columns.items():
        df = with_func(df, [column], lambda x, col: x[col].astype(float))
    return df


def as_string(df, columns=None):
    """
    Tranforms the given columns into strings
    :param df: Table to be transformed
    :param columns: dict
    columns to be transformed as keys, lenght of expected results as values
    :param lenght: columns to be transformed
    :return:
    """
    for column, lenght in columns.items():
        df = with_func(df, [column], lambda x, col: x[col].astype(str))
    return df


def all(df, as_strings=None, as_floats=None, as_set_len_codes=None, as_dates=None):
    df = as_string(df, columns=as_strings)
    df = as_float(df, columns=as_floats)
    df = as_set_len_code(df, columns=as_set_len_codes)
    df = as_date(df, columns=as_dates)

    return df
