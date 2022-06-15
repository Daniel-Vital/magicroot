

def cumsum(df, columns, by, order):
    return df.sort_values(order)[by + columns].groupby(by).cumsum()


def sum(df, columns, by):
    return df[by + columns].groupby(by).sum()

