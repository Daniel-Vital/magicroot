"""
This file contains the functions used to compute useful values for predetermined dataframe structures
"""
from . import format
from datetime import timedelta
import numpy as np
import pandas as pd


def duration(df, dt_begin, dt_end, computed_column='duration', days=False,  *args, **kwargs):
    """
    Computes duration in days between two dates
    :param df: Dataframe
        :column dt_begin: column(s) should be in the table
        :column dt_end: column(s) should be in the table
    base to compute

    :param dt_begin: str
    column with the begin date

    :param dt_end: str
    column with the end date

    :param computed_column: str, default 'maturity'
    column with the name to give to the column with the computed duration

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column duration_column: computed column
    result table
    """
    multiplier = 1 if days else 365
    return format.as_date(df, [dt_begin, dt_end],  *args, **kwargs).assign(
        **{
            computed_column: lambda x: np.maximum((x[dt_end] - x[dt_begin]).dt.days / multiplier, 0)
        }
    )


def date_perc(df, dt_begin, dt_end, dt_ref, duration_column='duration_pct',  *args, **kwargs):
    """
    Computes percentage of a date between to other dates
    :param df: Dataframe
        :column dt_begin: column(s) should be in the table
        :column dt_end: column(s) should be in the table
    base to compute

    :param dt_begin: str
    column with the begin date

    :param dt_end: str
    column with the end date

    :param dt_ref: str
    column with the end date

    :param duration_column: str, default 'maturity'
    column with the name to give to the column with the computed duration

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column duration_column: computed column
    result table
    """
    return format.as_date(df, [dt_begin, dt_end, dt_ref],  *args, **kwargs).assign(
        **{
            duration_column: lambda x:
            duration(x, dt_begin, dt_ref)['duration'] / duration(x, dt_begin, dt_end)['duration']
        }
    )


def maturity(df, ref_dt_column, cashflow_dt_column, maturity_column='maturity'):
    """
    Computes maturity
    :param df: Dataframe
        :column ref_dt_column: column(s) should be in the table
        :column cashflow_dt_column: column(s) should be in the table
    base to compute

    :param ref_dt_column: str
    column with the reference date

    :param cashflow_dt_column: str
    column with the cashflow date

    :param maturity_column: str, default 'maturity'
    column with the name to give to the column with the computed maturity

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column maturity_column: computed column
    result table
    """
    return format.as_date(df, [ref_dt_column, cashflow_dt_column]).assign(
        **{
            maturity_column: lambda x: np.maximum((x[cashflow_dt_column] - x[ref_dt_column]).dt.days / 365, 0)
        }
    )


def discount_rate(df, rate_column, maturity_column, disc_rate_column='disc_rate'):
    """
    Computes discount rate
    :param df: Dataframe
        :column ref_dt_column: column(s) should be in the table
        :column cashflow_dt_column: column(s) should be in the table
    base to compute

    :param rate_column: str
    column with the spot rate

    :param maturity_column: str
    column with the maturity

    :param disc_rate_column: str, default 'disc_rate'
    column with the name to give to the column with the computed discount rate

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column disc_rate_column: computed column
    result table
    """
    return df.assign(
        **{
            disc_rate_column: lambda x: 1 / (x[rate_column] + 1).pow(x[maturity_column])
        }
    )


def discounted_cashflows(df, cashflow_columns, disc_rate_column, prefix='disc_', suffix=''):
    """
    Discounts cashflows
    :param df: Dataframe
        :column cashflow_columns: column(s) should be in the table
        :column disc_rate_column: column(s) should be in the table
    base to compute

    :param cashflow_columns: list
    containing columns with cashflows to discount

    :param disc_rate_column: str
    Column with the discount rate

    :param prefix: str, default 'disc_'
    column with the prefix to add to the column names with the discounted cashflows

    :param suffix: str, default ''
    column with the suffix to add to the column names with the discounted cashflows

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column prefix + cashflow_columns: computed columns
    result table
    """
    return df.assign(
        **{
            prefix + column + suffix: df[column] * df[disc_rate_column]
            for column in cashflow_columns
        }
    )


def discounted_columns_pairs(cashflow_columns, prefix, suffix):
    """
    Computes a dictionary with the undiscounted version of columns as keys and the discounted version as values

    :param cashflow_columns: list
    undiscounted cashflow columns

    :param prefix: str
    prefix used to mark discounted columns

    :param suffix: str
     prefix used to mark discounted columns

    :return: a dictionary with the undiscounted version of columns as keys and the discounted version as values
    """
    return {
        undiscounted_column: prefix + undiscounted_column + suffix for undiscounted_column in cashflow_columns
    }


def discounted_components(df, cashflow_columns, prefix='comp_', suffix=''):
    """
    Computes discounted amounts from cashflows
    :param df: Dataframe
        :column cashflow_columns: column(s) should be in the table
    base to compute

    :param cashflow_columns: list
    containing columns with cashflows to discount

    :param prefix: str, default 'comp_'
    column with the prefix to add to the column names with the discounted amounts from cashflows

    :param suffix: str, default ''
    column with the suffix to add to the column names with the discounted cashflows

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column prefix + cashflow_columns: computed columns
    result table
    """
    return df.assign(
        **{
            prefix + disc_cashflow_column + suffix: lambda x: x[disc_cashflow_column] - x[cashflow_column]
            for cashflow_column, disc_cashflow_column in cashflow_columns.items()
        }
    )


def intersection_days(df, *args, intersection_column='intersection_dates'):
    """
    Computes the intersection days between all given time windows
    All windows should be provided in the format ('begin column', 'end column')
    :return:
    """
    return df.assign(
        **{
            intersection_column: lambda x: np.minimum(
                *[x[window[1]] for window in args]
            ) - np.maximum(
                *[x[window[0]] for window in args]
            )
        }
    )


def union_days(df, *args, union_column='union_dates'):
    """
    Computes the union days between all given time windows
    All windows should be provided in the format ('begin column', 'end column')
    :return:
    """
    return df.assign(
        **{
            union_column: lambda x: np.maximum(
                *[x[window[1]] for window in args]
            ) - np.minimum(
                *[x[window[0]] for window in args]
            )
        }
    )


def intersection_days_perc(df, *args, intersection_column='perc_intersection_dates', shift_days=0):
    """
    Computes the intersection days percentage between all given time windows
    All windows should be provided in the format ('begin column', 'end column')
    :return:
    """
    return df.assign(
        **{
            intersection_column: lambda x:
            (intersection_days(df, *args, intersection_column='intersection_dates')['intersection_dates'] + timedelta(days=shift_days)) /
            (union_days(df, union_column='union_dates', *args)['union_dates'] + timedelta(days=shift_days))
        }
    )


def eom(df, columns=None, prefix='eom_', suffix='', *args, **kwargs):
    return format.as_date(df, columns, *args, **kwargs).assign(
        **{
            prefix + column + suffix: lambda x: (x[column] - pd.to_timedelta(1, unit='day')) + pd.offsets.MonthEnd()
            for column in columns
        }
    )


