

def cumsum(columns, by, order):
    return lambda x: x.sort_values(by + order)[by + columns].groupby(by).cumsum()


def sum(columns, by):
    return lambda x: x[by + columns].groupby(by).sum().reset_index().merge(
        x.reset_index()[by], how='right', validate='one_to_many'
    )[columns]


def max(columns, by):
    return lambda x: x[by + columns].groupby(by).max().reset_index().merge(
        x.reset_index()[by], how='right', validate='one_to_many'
    )[columns]

