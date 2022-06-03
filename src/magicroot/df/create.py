import numpy as np
import pandas as pd


def empty(shape, *args, **kwargs):
    canvas = np.empty(shape)
    canvas[:] = np.NaN
    return pd.DataFrame(canvas, *args, **kwargs)


def const_col(df, const, *args, **kwargs):
    s = pd.Series(np.ones(len(df)) * const, *args, **kwargs)
    s.index = df.index
    return s
