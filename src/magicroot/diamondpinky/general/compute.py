from ...databranch.validation_tools.dataframe_shape import transform_columns_to_eu_dates
import numpy as np


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
    return transform_columns_to_eu_dates(df, [ref_dt_column, cashflow_dt_column]).assign(
        **{
            maturity_column: lambda x: np.maximum((x[cashflow_dt_column] - df[ref_dt_column]).dt.days / 365, 0)
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


def discount_cashflows(df, cashflow_columns, disc_rate_column, prefix='disc_'):
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

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column prefix + cashflow_columns: computed columns
    result table
    """
    return df.assign(
        **{
            column + prefix: lambda x: x[column] * x[disc_rate_column]
            for column in cashflow_columns
        }
    )


def discounted_components(df, cashflow_columns, prefix='comp_'):
    """
    Computes discounted amounts from cashflows
    :param df: Dataframe
        :column cashflow_columns: column(s) should be in the table
    base to compute

    :param cashflow_columns: list
    containing columns with cashflows to discount

    :param prefix: str, default 'comp_'
    column with the prefix to add to the column names with the discounted amounts from cashflows

    :return: Dataframe
        :column previous: all column(s) previously in the table
        :column prefix + cashflow_columns: computed columns
    result table
    """
    return df.assign(
        **{
            disc_cashflow_column + prefix: lambda x: x[disc_cashflow_column] - x[cashflow_column]
            for cashflow_column, disc_cashflow_column in cashflow_columns.items()
        }
    )