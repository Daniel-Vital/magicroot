import numpy as np
import pandas as pd


def empty(shape, *args, **kwargs):
    canvas = np.empty(shape)
    canvas[:] = np.NaN
    return pd.DataFrame(canvas, *args, **kwargs)

