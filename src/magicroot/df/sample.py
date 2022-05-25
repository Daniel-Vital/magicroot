import pandas as pd
from . import select
import logging

log = logging.getLogger(__name__)


def columns_in_list(df, columns, n=1):
    common_columns = select.columns_in_list(df, columns=columns)
    key = df[common_columns].drop_duplicates().sample(n).to_dict('list')
    return df[df[common_columns].isin(key).all(axis=1)]


def join(*args, on, n=1):
    result = []
    df_sample = pd.DataFrame()
    for i, df in enumerate(args):
        if i == 0:
            df_sample = columns_in_list(df, columns=on, n=n)
        else:
            columns_in_previous = select.columns_in_list(df_sample, columns=on)
            columns_in_current = select.columns_in_list(df, columns=on)
            common_columns = list({*columns_in_previous}.intersection({*columns_in_current}))
            key = df_sample[common_columns].drop_duplicates().to_dict('list')
            df_sample = df[df[common_columns].isin(key).all(axis=1)]
        result.append(df_sample)

    return result


def simple_join(left, right, on, n=1, *args, **kwargs):
    left, right = join(left, right, on=on, n=n)
    joined = left.merge(right, on=on, *args, **kwargs)
    return left, right, joined
