

def cumsum(columns, by, order):
    return lambda x: x.sort_values(by + order)[by + columns].groupby(by).cumsum()


def sum(columns, by):
    return lambda x: x[by + columns].groupby(by).sum()

