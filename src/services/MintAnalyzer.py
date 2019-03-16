import datetime
import errno
import os
import os.path
import sys

import pandas as pd

from . import MintHistoryReader

# region Constants

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

# endregion

# region Helper Functions


def mkdir_p(path):
    """
    Creates the parent directories if they do not exist.

    :param path: The directory path to create
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# endregion


class MintAnalyzer(object):
    """
    Exposes methods for advanced analysis on Intuit Mint data
    """

    def __init__(self):
        self.mint_history_reader = MintHistoryReader.MintHistoryReader()

    def get_transactions_per_paycheck(self):
        """
        Get a dictionary of transactions per pay period keyed by pay date where the value is a pandas DataFrame
        """
        transactions = self.mint_history_reader.get_latest_transactions()

        # Get paycheck dates
        transactions = transactions.set_index(['date'])
        paychecks = transactions[transactions['category'] == 'paycheck']
        paycheck_dates = paychecks.index

        # Get a dictionary of transactions keyed by pay period
        transactions_per_pay_period = {}
        for i in range(len(paycheck_dates) - 1):
            transactions_in_period = transactions.loc[paycheck_dates[i]:paycheck_dates[i + 1]]
            transactions_in_period = transactions_in_period.drop(paycheck_dates[i])
            transactions_per_pay_period[paycheck_dates[i + 1]] = transactions_in_period

        return transactions_per_pay_period

    def save_transactions_per_paycheck(self):
        """
        Writes a file for each pay period showing the transactions that were made during it

        :param transactions: the pandas DataFrame of all transactions
        :param transactions_per_paycheck: the dictionary of transactions per pay period
                keyed by pay date where the value is a pandas DataFrame
        """
        transactions_per_paycheck = self.get_transactions_per_paycheck()

        # Write transactions to file for each pay date
        for pay_date, transactions_in_period in transactions_per_paycheck.items():
            file_path = "history/%s/SpendingPerPaycheck/%s/" % (TODAY, pay_date)
            mkdir_p(file_path)
            outfile_name = "%sTransactions.csv" % file_path
            print("Saving transactions for paycheck %s to %s..." % (pay_date, outfile_name))
            pd.DataFrame.to_csv(transactions_in_period, outfile_name)
        print("Saved transactions for paycheck\n")

    def get_spending_per_paycheck_per_category(self):
        """
        Get a dictionary keyed by pay date where the value is
        a pandas DataFrame of amount spent per transaction category for that paycheck

        :param transactions: the pandas DataFrame of all transactions
        :param transactions_per_paycheck: the dictionary of transactions per paycheck
                keyed by pay date where the value is a pandas DataFrame
        """
        transactions_per_paycheck = self.get_transactions_per_paycheck()

        # Get the amount spent per category for each paycheck
        spending_per_category_per_pay_period = {}
        for pay_date, transactions_in_period in transactions_per_paycheck.items():
            transactions_by_category = transactions_in_period.groupby('category').sum()
            amount_per_category = transactions_by_category['amount']
            spending_per_category_per_pay_period[pay_date] = amount_per_category

        return spending_per_category_per_pay_period

    def save_spending_per_paycheck_per_category(self):
        """
        Writes a file for each pay period showing the amount spent per category

        :param spending_per_category_per_paycheck: the dictionary keyed by pay date where the value is
                a pandas DataFrame of amount spent per transaction category for that paycheck
        """
        spending_per_category_per_paycheck = self.get_spending_per_paycheck_per_category()

        # Write amount spent per category to file for each pay date
        for pay_date, amount_spent_per_category in spending_per_category_per_paycheck.items():
            file_path = "history/%s/SpendingPerPaycheck/%s/" % (TODAY, pay_date)
            mkdir_p(file_path)
            outfile_name = "%sCategories.csv" % file_path
            print("Saving amount spent per category for paycheck %s to %s..." % (pay_date, outfile_name))
            outfile = open(outfile_name, "w")
            print(amount_spent_per_category, file=outfile)

        print("Saved amount spent per category per paycheck\n")

    def get_account_balances_over_time(self):
        """
        Get a dictionary keyed by (account_provider,account_name) where the value is
        a dictionary containing a list of retrieval dates and a list of associated balances {'dates': [YYYY-MM-DD], 'balances': [$]}.
        Accounts of type 'credit' have their balances turned negative.

        :param transactions: a dictionary keyed by (account_provider,account_name) where the value is 
        a dictionary containing a list of retrieval dates and a list of associated balances {'dates': [YYYY-MM-DD], 'balances': [$]}
        """
        account_history = self.mint_history_reader.get_accounts_over_time()

        # Get accounts
        first_key = list(account_history.keys())[0]
        account_providers = account_history[first_key]['provider']
        account_names = account_history[first_key]['name']
        
        # Initialize dictionaries 
        # TODO: Prepare for not all account_snapshots to have the same providers
        account_balances_over_time = {}
        for i in range(len(account_providers)):
            account_balances_over_time['%s,%s' % (account_providers[i], account_names[i])] = {'dates': [], 'balances': []}

        # Get {'dates': [YYYY-MM-DD], 'balances': [$]} per account for all dates
        for date, account_snapshot in account_history.items():
            for i in range(len(account_providers)):
                # Get Balance for this Account For this account_snapshot
                account_provider = account_providers[i]
                account_name = account_names[i]
                rows_with_that_provider = account_snapshot.loc[account_snapshot['provider'] == account_provider]
                row_with_that_name = rows_with_that_provider.loc[rows_with_that_provider['name'] == account_name]
                balance = row_with_that_name.iloc[0]['balance']

                # Make accounts of type 'credit' negative
                account_type = row_with_that_name.iloc[0]['type']
                if account_type == 'credit':
                    balance = balance * -1

                # Store date & balance for this account_snapshot
                account_balances_over_time['%s,%s' % (account_provider, account_name)]['dates'].append(date)
                account_balances_over_time['%s,%s' % (account_provider, account_name)]['balances'].append(balance)

        return account_balances_over_time

    def get_credit_score_over_time(self):
        """
        Get a dictionary keyed by date retrieved where the value is the credit score at that time.
        Credit Scores that cannot be cast to an integer get removed from the dictionary.
        """
        credit_history = self.mint_history_reader.get_credit_score_over_time()
        credit_history_copy = dict(credit_history)

        # Ensure the credit score is an integer
        for date, score in credit_history.items():
            try:
                _ = int(score)
            except ValueError:
                # credit score is invalid (Probably is a string saying "No credit score provided.")
                del credit_history_copy[date]
                pass

        return credit_history_copy

# region Test the Class

# print("\n===================================================================")
# print("MintAnalyzer test")
# print("===================================================================\n")

# mint_analyzer = MintAnalyzer(None)

# print("transactions_per_paycheck:")
# print(mint_analyzer.get_transactions_per_paycheck())

# print("\nspending_per_category_per_paycheck:")
# print(mint_analyzer.get_spending_per_category_per_paycheck())

# print("\naccount_balances_over_time:")
# print(mint_analyzer.get_account_balances_over_time())

# print("\ncredit_score_over_time:")
# print(mint_analyzer.get_credit_score_over_time())

# endregion