

def column_name_sequence(df, sequence):
    """
    Removes a sequence in the column names of a Dataframe
    :param df:
    :param sequence:
    :return:
    """
    df.columns = [column.replace(sequence, '') for column in df.columns]
    return df
