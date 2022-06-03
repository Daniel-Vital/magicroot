import pandas as pd


def fillna(index, level, value):
    level = 1  # TODO colocar a funcionar para qualquer nivel
    return pd.MultiIndex.from_tuples([col if col[level] != '' else (value, col[0]) for col in index.values])


