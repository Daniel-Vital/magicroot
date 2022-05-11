from . import compute
import logging

log = logging.getLogger(__name__)


def cashflows(
        df_cashflows,
        ref_dt_column,
        cashflow_dt_column,
        rate_column,
        cashflow_columns,
        maturity_column=None,
        disc_rate_column=None,
        discounted_prefix=None,
        component_prefix=None
):
    """
    Merges cashflows and discount rates tables, and calls with_single_table to discount cashflows
    :param df_cashflows: Dataframe
        :column on: column(s) should be in the table
    to be discounted

    :param df_discount_rates: Dataframe
        :column on: column(s) should be in the table
    with discount rates

    :param on: str
    See pandas.DataFrame.merge parameter on

    :return: See with_single_table
    """
    df_cashflows = compute.maturity(df_cashflows, ref_dt_column, cashflow_dt_column, maturity_column)
    df_cashflows = compute.discount_rate(df_cashflows, rate_column, maturity_column, disc_rate_column)
    df_cashflows = compute.discounted_cashflows(df_cashflows, cashflow_columns, disc_rate_column, discounted_prefix)
    discounted_columns_pairs = compute.discounted_columns_pairs(cashflow_columns, discounted_prefix)
    df_cashflows = compute.discounted_components(df_cashflows, discounted_columns_pairs, component_prefix)

    return df_cashflows


def by_cashflow_date(
        df_cashflows,
        df_discount_rates,
        ref_dt_column,
        cashflow_dt_column,
        maturity_column,
        *args, **kwargs
):
    """
    Computes maturity, and calls by_maturity to discount cashflows
    :param df_cashflows: Dataframe
        :column ref_dt_column: column(s) should be in the table
        :column cashflow_dt_column: column(s) should be in the table
    to be discounted

    :param df_discount_rates: Dataframe
        :column ref_dt_column: column(s) should be in the table
        :column cashflow_dt_column: column(s) should be in the table
    with discount rates

    :param ref_dt_column: str
    column with the reference date

    :param cashflow_dt_column: str
    column with the cashflow date

    :param maturity_column: str, default 'maturity'
    column with the name to give to the column with the computed maturity

    :return: See with_single_table
    """
    log.debug('Computing maturity')
    df_cashflows = compute.maturity(
        df=df_cashflows,
        ref_dt_column=ref_dt_column, cashflow_dt_column=cashflow_dt_column, maturity_column=maturity_column
    )
    df_discount_rates = compute.maturity(
        df=df_discount_rates,
        ref_dt_column=ref_dt_column, cashflow_dt_column=cashflow_dt_column, maturity_column=maturity_column
    )

    return by_maturity(
        df_cashflows=df_cashflows, df_discount_rates=df_discount_rates,
        maturity_column=maturity_column, *args, **kwargs
    )


def by_maturity(df_cashflows, df_discount_rates, on, *args, **kwargs):
    """
    Merges cashflows and discount rates tables, and calls with_single_table to discount cashflows
    :param df_cashflows: Dataframe
        :column on: column(s) should be in the table
    to be discounted

    :param df_discount_rates: Dataframe
        :column on: column(s) should be in the table
    with discount rates

    :param on: str
    See pandas.DataFrame.merge parameter on

    :return: See with_single_table
    """
    df = df_cashflows.merge(right=df_discount_rates, how='left', on=on)

    return with_single_table(df, *args, **kwargs)


def with_single_table(df, rate_column, maturity_column, *args, **kwargs):
    """
    Creates a column with the discounted rate, and calls with_discounted_rates to discount cashflows
    :param df: Dataframe
        :column rate_column: column(s) should be in the table
        :column maturity_column: column(s) should be in the table
    to be discounted

    :param rate_column: str
    column with the spot rate

    :param maturity_column: str
    column with the maturity

    :return: See with_discounted_rates
    """
    df = compute.discount_rate(df=df, rate_column=rate_column, maturity_column=maturity_column)

    return with_discounted_rates(df=df, *args, **kwargs)


def with_discounted_rates(
        df,
        cashflow_columns,
        disc_rate_column,
        prefix='disc_',
        components=False
):
    """
    Creates columns with the discounted cashflows
    :param df: Dataframe
        :column cashflow_columns: column(s) should be in the table
        :column disc_rate_column: column(s) should be in the table
    to be discounted

    :param cashflow_columns: list
    containing columns with cashflows to discount

    :param disc_rate_column: str
    Column with the discount rate

    :param prefix: str, default 'disc_'
    Prefix for the discounted columns

    :param components: str or bool, default False
    If True, adds a columns to the output DataFrame with prefix 'comp_' with discounted components.

    :return: Table with discounted cashflows
        :column cashflow_columns: All columns in the index should be in the table
        :column disc_rate_column: Amount of each cashflow
        :column prefix + cashflow_columns: cashflow discounted
        :column components + prefix + cashflow_columns: Amount of each cashflow that was discounted
    """
    df = compute.discounted_cashflows(
        df=df, cashflow_columns=cashflow_columns, disc_rate_column=disc_rate_column, prefix=prefix
    )

    if components:
        components = components if isinstance(components, str) else 'comp_'
        components_pairs = {column: prefix + column for column in cashflow_columns}
        df = compute.discounted_components(
            df=df, cashflow_columns=components_pairs, prefix=components
        )

    return df
