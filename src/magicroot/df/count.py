from . import add as _add


def unique(df, values, by, prefix='Count_', *args, **kwargs):
    df = df[
        by + values
    ].drop_duplicates().groupby(by, dropna=False).count().sort_values(values, ascending=False).reset_index()
    return _add.column_name(df, to_columns=values, prefix=prefix, *args, **kwargs)
    

