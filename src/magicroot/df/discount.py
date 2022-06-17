from . import compute
import logging

log = logging.getLogger(__name__)


def component(
        cashflows, from_date, to_date, with_rate
):
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
    return cashflows(with_rate=with_rate, from_date=from_date, to_date=to_date) - cashflows


def cashflows(
        cashflows, from_date, to_date, with_rate
):
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
    return cashflows * factor(
        with_rate=with_rate, with_maturity=compute.maturity(from_date=from_date, to_date=to_date)
    )


def factor(with_rate, with_maturity, days_in_year=365):
    """
    Computes discount rate

    :param with_rate: str
    Series with the spot rate

    :param with_maturity: str
    Series with the maturity

    :param days_in_year: int
    constant with the days in the year

    :return: func to be applied to a Dataframe
    """
    return 1 / (1 + with_rate).pow(with_maturity.dt.days / days_in_year)

