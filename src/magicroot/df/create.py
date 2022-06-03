import numpy as np
import pandas as pd


def empty(shape, *args, **kwargs):
    canvas = np.empty(shape)
    canvas[:] = np.NaN
    return pd.DataFrame(canvas, *args, **kwargs)


def const_col(df, const, *args, **kwargs):
    canvas = np.ones(len(df)) * const
    return pd.Series(canvas, *args, **kwargs)
