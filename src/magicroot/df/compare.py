import pandas as pd
from .reshape import uniformize_columns
from .select import numeric_columns


def grouped(df_tested, df_benchmark, by, *args, **kwargs):
    """
    Compares two grouped versions of a pair of dataframes
    :param df_tested:
    :param df_benchmark:
    :param by:
    :return:
    """

    def group_func(df):
        return df.groupby(by).sum().reset_index()

    df_tested = group_func(df_tested)
    df_benchmark = group_func(df_benchmark)

    return dataframes(df_tested, df_benchmark, by, *args, **kwargs)


def types(*args):
    """
    Compares types of in a list fields
    :param args: list of Dataframes
    :return: Dataframe with comparison of types
    """
    return pd.DataFrame({
        'df_' + str(i + 1): df.dtypes for i, df in enumerate(args)
    })


def dataframes(df_tested, df_benchmark, index, names=('Tested', 'Benchmark')):
    """
    Transforms both dataframes such that the method DataFrame.compare can be used
    :param df_tested:
    :param df_benchmark:
    :param index:
    :param names:
    :return:
    """
    df_tested, df_benchmark = uniformize_columns(df_tested, df_benchmark)
    index_values = df_tested[index].merge(df_benchmark[index], how='outer').drop_duplicates().reset_index(drop=True)
    df_tested = index_values.merge(df_tested, how='left')
    df_benchmark = index_values.merge(df_benchmark, how='left')

    result = df_tested.compare(
        df_benchmark, align_axis=0, keep_shape=True, keep_equal=True
    )

    result = result.reset_index().rename(
        columns={'level_0': 'LINE', 'level_1': 'SOURCE'}
    )

    group = result.groupby(index + ['LINE'], dropna=False)[numeric_columns(result, remove='LINE')].fillna(0)

    def treat_result(df, name):
        return pd.concat([result[['LINE', 'SOURCE']], df], axis=1).query('SOURCE == "other"').assign(SOURCE=name)

    a = treat_result(group.diff().abs(), 'Abs diff')
    b = treat_result(group.pct_change(), 'Rel diff')

    result = pd.concat([result, a, b])

    sorter = {'self': '01', 'other': '02', 'Abs diff': '03', 'pct diff': '04'}
    sorter = {key: value + ' ' + key for key, value in sorter.items()}

    result = result.assign(
        SORTER_SOURCE=lambda x: x['SOURCE'].replace(sorter),
        SORTER_LINE=lambda x: x['LINE'].astype(str).str.zfill(len(x['LINE'].max().astype(str))),
        SORTER=lambda x: x['SORTER_LINE'] + x['SORTER_SOURCE']
    ).sort_values(by='SORTER').drop(columns=['SORTER_SOURCE', 'SORTER_LINE', 'SORTER'])

    result = result.assign(
        SOURCE=lambda x: x['SOURCE'].mask(x['SOURCE'] == 'self', names[0]).mask(x['SOURCE'] == 'other', names[1])
    )

    result[index] = result[index].fillna(method='ffill')

    result = result.round(2)
    return result
