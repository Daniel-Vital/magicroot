import pandas as pd
import logging as log
from ...smartowl.partiallyorderedset import PartiallyOrderedSet


class EventsDataFrame(pd.DataFrame):
    """

    """
    def __init__(self, *args, **kwargs):
        super().__init__(columns=['Datetime', 'Value'], *args, **kwargs)


class Account:
    """
    Something that holds value
    """
    value = 0

    @property
    def id(self):
        return hash(self)

    def __hash__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        pass


class CashFlow:
    """
    Movement between accounts, from credit account to debit account
    """
    value = 0.0
    debit = 0
    credit = 0


account_1 = Account()
account_2 = Account()

cf = CashFlow()

x = ['Balance', 'Profit_Loss']
y = ['Asset', 'Liability', 'Profit', 'Loss']


class ChartOfAccounts(PartiallyOrderedSet):
    def __init__(
            self,
            from_dict=None,
            from_dataframe=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

    def from_dict(self, data, *args, **kwargs):
        pass


accounts = {
    # level 1
    'Balance': None,
    'Profit_Loss': None,
    # level 2
    'Asset': 'Balance',
    'Liability': 'Balance',
    'Profit': 'Profit_Loss',
    'Loss': 'Profit_Loss',
    # level 3
    'Cash': 'Asset',
    'Stock': 'Asset',
    'Option': 'Asset',
    'Margin': 'Liability',
    'Stock Gains Realized': 'Profit',
}


def define_event(event, ticker, operator):
    if event == 'BUY_STOCK':
        return ['Balance', 'Asset', 'Cash Long'], ['Balance', 'Asset', 'Stock Long']


events = {
    'Some event':
        ['Cashflow 1', 'Cashflow 2'],
    'Second event':
        ['Other CashFlow']
}

"""
EventLedger
LedgerID    |   DateTime   |   Event   |   ...  |   Value


Event -> Several CashFlows

types Cashflows:
    Actual
    Expected

Event -> DateTime, Debit Account, Credit Account, Value
DateTime, Debit Account, Credit Account, Value - I am calling a Cash Flow

CashFlowLedger
LedgerID    |   DateTime   |   Debit Account   |   Credit Account  |   Value




"""


