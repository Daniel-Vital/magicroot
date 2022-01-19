
# Imports
import pandas as pd
import numpy as np
import logging as log
log = log.getLogger('BSheet')


class BalanceSheet:
    def __init__(self, events, tickers, operators, default_operator='Bank'):
        self.events = events
        # Creates balance Dataframe
        df_balance_sheet = self.accounts_from_events().merge(
            # Multiplies lines for each Ticker
            pd.DataFrame(np.array(tickers), columns=['Ticker']),
            how='cross'
        ).merge(
            # Multiplies lines for each Operator
            pd.DataFrame(np.array(operators + [default_operator]), columns=['Operator']),
            how='cross'
        ).assign(
            # Creates columns for balances
            Opening_Balance=0.0,
            Debit_Balance=0.0,
            Credit_Balance=0.0,
            Closing_Balance=0.0
        ).set_index([
            # Creates and sorts index and saves table in the staging area
            'Account_1',
            'Account_2',
            'Account_3',
            'Ticker',
            'Operator'
        ]).sort_index()

        self.__data = df_balance_sheet

    def __update(self):
        self.__data = self.__data.assign(
            Closing_Balance=lambda x: x['Debit_Balance'] - x['Credit_Balance']
        )

    def __posted_accounts(self):
        return self.__data.loc[
            self.__data['Opening_Balance'].abs() +
            self.__data['Credit_Balance'].abs() +
            self.__data['Debit_Balance'].abs() +
            self.__data['Closing_Balance'].abs() > 0
            ]

    def __str__(self):
        self.__update()
        return self.__posted_accounts().__str__()

    def to_csv(self, *args, **kargs):
        self.__posted_accounts().to_csv(*args, **kargs)

    def post(self, value, credit_account=None, debit_account=None, event=None, ticker=None, operator=None):
        if event is not None and ticker is not None and operator is not None:
            credit_account = self.load_account(event, ticker, operator, credit=True)
            debit_account = self.load_account(event, ticker, operator, credit=False)
        if credit_account is not None and debit_account is not None:
            log.debug('\t\t Posting on Balance Sheet: moving {} from {} to {}'
                      .format(value, credit_account, debit_account))
            self.credit(value, credit_account)
            self.debit(value, debit_account)
        else:
            log.warning('\t\t Cannot post with given inputs, please provide:'
                        '\t\t\t (value, credit_account, debit_account) or '
                        '\t\t\t (value, event, ticker, operator)')
        return debit_account, credit_account

    def credit(self, value, account):
        self.__data.loc[
            account[0],
            account[1],
            account[2],
            account[3],
            account[4]
        ].at['Credit_Balance'] += abs(value)
        self.__update()

    def debit(self, value, account):
        self.__data.loc[
            account[0],
            account[1],
            account[2],
            account[3],
            account[4]
        ].at['Debit_Balance'] += abs(value)
        self.__update()

    def load_account(self, event, ticker=None, operator=None, credit=True):
        movement = 'CREDIT' if credit else 'DEBIT'
        log.debug('\t\t Loading {}(movement) account for {}(event) {}(ticker) on {}(operator)'
                  .format(movement, event, ticker, operator))
        account = self.events[event][movement].copy()
        log.debug('\t\t\t Account before attribution {}'.format(account))
        try:
            if account[-2] is None:
                log.debug('\t\t\t Attributing appropriate ticker {}'.format(ticker))
                account[-2] = ticker if ticker is not None else log.warning('\t\t Account loaded incorrectly')
            if account[-1] is None:
                log.debug('\t\t\t Attributing appropriate operator {}'.format(operator))
                account[-1] = operator if operator is not None else log.warning('\t\t Account loaded incorrectly')
        except IndexError as err:
            log.error('\t\t Event {}(event) account {}(movement) could not be loaded'.format(event, movement))
            raise err
        log.debug('\t\t\t Loaded {}'.format(account))
        return account

    def operator(self, operator):
        print(self.__data.reset_index().loc[operator])

    def accounts_from_events(self, keep_only_main_accounts=True):
        defined_accounts = []
        for key in self.events:
            defined_accounts.append(self.events[key]['CREDIT'])
            defined_accounts.append(self.events[key]['DEBIT'])

        df = pd.DataFrame(np.array(defined_accounts), columns=[
            'Account_1', 'Account_2', 'Account_3', 'Operator', 'Ticker'
        ])

        if keep_only_main_accounts:
            df = df[['Account_1', 'Account_2', 'Account_3']].drop_duplicates()

        return df


