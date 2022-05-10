import pandas as pd


def as_date(df, columns):
    """
    Tranforms the given columns into european dates in the given table
    :param df: Table to be transformed
    :param columns: columns to be transformed
    :return:
    """
    return df.assign(
        **{
            column: lambda x: pd.to_datetime(
                x[column],
                errors='coerce'
            ) for column in columns
        }
    )