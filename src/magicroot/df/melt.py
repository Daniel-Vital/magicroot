"""
This file contains the functions used to create new lines based on the values of a single row
"""
import pandas as pd
from . import format


def date_interval(
        df, begin_dt_column, end_dt_column,
        freq='M',
        period_column='period',
        begin_period_column='begin_period',
        end_period_column='end_period',
        *args, **kwargs):
    offset = pd.offsets.MonthEnd() if freq == 'M' else pd.offsets.YearEnd()
    return format.as_date(df[[begin_dt_column, end_dt_column]], columns=None, *args, **kwargs).apply(
        lambda x: pd.Series(
            pd.date_range(
                start=x[begin_dt_column],
                end=(x[end_dt_column] - pd.to_timedelta(1, unit='day')) + offset,
                freq=freq
            )
        ), axis=1
    ).stack().reset_index(level=-1, name=begin_period_column).rename(columns={'level_1': period_column}).assign(
        **{
            begin_period_column: lambda x: x[begin_period_column].to_numpy().astype('datetime64[M]'),
            end_period_column: lambda x: x[begin_period_column] + pd.offsets.MonthEnd()
        }
    ).join(df)


