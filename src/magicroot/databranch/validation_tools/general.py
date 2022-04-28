

def check_indexes(df, index):
    """
    Returns all duplicated lines of a dataframe for a given index
    :param df:
    :param index:
    :return:
    """
    return df[df[index].duplicated(keep=False)].sort_values(index)


def compared_grouped(df_base, df_new, by, target_columns, diff_columns_suffixe='DIFF_'):
    """
    Compares two grouped versions of a pair of dataframes
    :param df_base:
    :param df_new:
    :param by:
    :param target_columns:
    :param diff_columns_suffixe:
    :return:
    """

    def group_func(df):
        return df.groupby(by).sum().reset_index()

    df_base = group_func(df_base)
    df_new = group_func(df_new)

    def diff(column):
        return lambda df: df[column + '_new'] - df[column]

    return df_base.merge(df_new, how='outer', validate='one_to_one', suffixes=('', '_new'), on=by).assign(
        **{
            diff_columns_suffixe + target_column: diff(target_column)
            for target_column in target_columns
        }
    ).sort_values(by=[diff_columns_suffixe + target_column for target_column in target_columns], ascending=False)
