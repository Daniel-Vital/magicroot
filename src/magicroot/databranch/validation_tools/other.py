
def check_indexes(df, index):
    """
    Returns all duplicated lines of a dataframe for a given index
    :param df:
    :param index:
    :return:
    """
    return df[df[index].duplicated(keep=False)].sort_values(index)

