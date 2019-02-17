import datetime
import errno
import os
import os.path

import pandas as pd

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
    """Exposes methods for advanced analysis on Intuit Mint data"""

    def __init__(self, mint_manager):
        self.mint = mint_manager

    def get_transactions_per_paycheck(self, transactions=None):
        """
        Get a dictionary of transactions per pay period keyed by pay date where the value is a pandas DataFrame
        """
        print("Getting transactions per pay period...")
        if transactions is None:
            transactions = self.mint.get_transactions()
        transactions = transactions.set_index(['date'])

        # Get paycheck dates
        paychecks = transactions[transactions['category'] == 'paycheck']
        paycheck_dates = paychecks.index

        # Get a dictionary of transactions keyed by pay period
        transactions_per_pay_period = {}
        for i in range(len(paycheck_dates) - 1):
            transactions_in_period = transactions.loc[paycheck_dates[i]:paycheck_dates[i + 1]]
            transactions_in_period = transactions_in_period.drop(paycheck_dates[i])
            transactions_per_pay_period[paycheck_dates[i + 1].strftime("%Y-%m-%d")] = transactions_in_period

        return transactions_per_pay_period

    def save_transactions_per_paycheck(self, transactions=None, transactions_per_paycheck=None):
        """
        Writes a file for each pay period showing the transactions that were made during it

        :param transactions: the pandas DataFrame of all transactions
        :param transactions_per_paycheck: the dictionary of transactions per pay period
                keyed by pay date where the value is a pandas DataFrame
        """
        if transactions_per_paycheck is None:
            if transactions is None:
                transactions_per_paycheck = self.get_transactions_per_paycheck()
            else:
                transactions_per_paycheck = self.get_transactions_per_paycheck(transactions)

        # Write transactions to file for each pay date
        for pay_date, transactions_in_period in transactions_per_paycheck.items():
            file_path = "history/%s/SpendingPerPaycheck/%s/" % (TODAY, pay_date)
            mkdir_p(file_path)
            outfile_name = "%sTransactions.csv" % file_path
            print("Saving transactions for paycheck %s to %s..." % (pay_date, outfile_name))
            pd.DataFrame.to_csv(transactions_in_period, outfile_name)
        print("Saved transactions for paycheck\n")

    def get_spending_per_category_per_paycheck(self, transactions=None, transactions_per_paycheck=None):
        """
        Get a dictionary keyed by pay date where the value is
        a pandas DataFrame of amount spent per transaction category for that paycheck

        :param transactions: the pandas DataFrame of all transactions
        :param transactions_per_paycheck: the dictionary of transactions per paycheck
                keyed by pay date where the value is a pandas DataFrame
        """
        if transactions_per_paycheck is None:
            if transactions is None:
                transactions_per_paycheck = self.get_transactions_per_paycheck()
            else:
                transactions_per_paycheck = self.get_transactions_per_paycheck(transactions)

        # Get the amount spent per category for each paycheck
        spending_per_category_per_pay_period = {}
        for pay_date, transactions_in_period in transactions_per_paycheck.items():
            transactions_by_category = transactions_in_period.groupby('category').sum()
            amount_per_category = transactions_by_category['amount']
            spending_per_category_per_pay_period[pay_date] = amount_per_category

        return spending_per_category_per_pay_period

    def save_spending_per_category_per_paycheck(self, spending_per_category_per_paycheck=None):
        """
        Writes a file for each pay period showing the amount spent per category

        :param spending_per_category_per_paycheck: the dictionary keyed by pay date where the value is
                a pandas DataFrame of amount spent per transaction category for that paycheck
        """
        if spending_per_category_per_paycheck is None:
            spending_per_category_per_paycheck = self.get_spending_per_category_per_paycheck()

        # Write amount spent per category to file for each pay date
        for pay_date, amount_spent_per_category in spending_per_category_per_paycheck.items():
            file_path = "history/%s/SpendingPerPaycheck/%s/" % (TODAY, pay_date)
            mkdir_p(file_path)
            outfile_name = "%sCategories.csv" % file_path
            print("Saving amount spent per category for paycheck %s to %s..." % (pay_date, outfile_name))
            outfile = open(outfile_name, "w")
            print(amount_spent_per_category, file=outfile)

        print("Saved amount spent per category per paycheck\n")

