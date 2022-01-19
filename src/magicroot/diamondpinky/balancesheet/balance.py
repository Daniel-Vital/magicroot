"""
A Class to handle the balance sheet

"""
import pandas as pd

from . import balancesheet as Bal
import logging as log

log = log.getLogger('Balance')


class Balance:

    def __init__(self, tickers, operators, events, output_balance_sheet, output_positions, output_accounts):
        log.debug('\t Creating balance sheet')
        self.Sheet = Bal.BalanceSheet(events, tickers, operators)
        log.debug('\t Creating positions sheet')
        self.Positions = Bal.BalanceSheet(events, tickers, operators)

        self.events = pd.DataFrame()
        self.output_balance_sheet = output_balance_sheet
        self.output_positions = output_positions
        self.output_accounts = output_accounts
        self.to_csv()

    def to_csv(self):
        """
        Saves the balance on the staging area
        :return:
        """
        log.debug('\t Saving balance sheet and positions sheet to staging area')
        self.Sheet.to_csv(self.output_balance_sheet)
        self.Positions.to_csv(self.output_positions)
        self.Sheet.accounts_from_events().to_csv(self.output_accounts)

    def post(self, df_events):
        self.events = df_events

        debit = []
        credit = []

        for i, (index, row) in enumerate(df_events.reset_index().iterrows()):
            if row is not None:
                log.debug('\t Preparing to post event {} of {}'.format(i + 1, df_events.count()[0]))
                debit_account, credit_account = \
                    self.Sheet.post(value=row.Value, event=row.Event, ticker=row.Ticker, operator=row.Operator)
                debit.append(debit_account.__str__())
                credit.append(credit_account.__str__())
                self.Positions.post(value=row.Units, event=row.Event, ticker=row.Ticker, operator=row.Operator)

        self.events.insert(1, 'Debit Account', debit)
        self.events.insert(1, 'Credit Account', credit)
        self.to_csv()

    def audit(self, account, output_audit=None, filter_relevant_values=False):
        log.debug('\t Running audit on account {}'.format(account))
        audit = self.events.reset_index()
        audit.assign(Audit_Value=0).loc[
            (audit['Debit Account'] != account.__str__()) &
            (audit['Credit Account'] != account.__str__()),
            'Audit_Value'
        ] = 0
        audit.loc[audit['Credit Account'] == account.__str__(), 'Audit_Value'] = -1 * audit['Value']
        audit.loc[audit['Debit Account'] == account.__str__(), 'Audit_Value'] = 1 * audit['Value']
        if filter_relevant_values:
            audit = audit[
                lambda x: x['Audit_Value'] != 0
            ].drop(['Debit Account', 'Credit Account'], axis=1)
        if output_audit is not None:
            log.debug('\t\t Saving audit to {}'.format(output_audit))
            audit.to_csv(output_audit)
        return audit


