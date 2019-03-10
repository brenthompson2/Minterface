import datetime
import errno
import os
import os.path

import mintapi
import pandas as pd

# region Constants

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

# endregion

# region Helper Functions


# Taken from https://stackoverflow.com/questions/23793987/write-file-to-a-directory-that-doesnt-exist
def safe_open_w(path):
    """
    Open path for writing, creating any parent directories as needed.

    :param path: The directory path to safely open
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return open(path, 'w')


# endregion


class MintManager(object):
    """Exposes methods for getting or saving Intuit Mint data"""

    def __init__(self, user, pwd):
        """Login to Mint and refresh account data"""
        print("Connecting to Mint...\nIt may take a couple minutes to login and refresh all account data...")
        self.mint = mintapi.Mint(
            user,
            pwd
        )
        print("Connected\n")

    def __del__(self):
        self.mint.close()

    def get_accounts(self):
        """Get a list of account data"""
        print("Getting accounts...")
        return self.mint.get_accounts()

    def save_accounts(self, accounts=None):
        """Write the account data to a file"""
        if accounts is None:
            accounts = self.get_accounts()

        outfile_name = str("history/%s/Accounts.csv" % TODAY)
        outfile = safe_open_w(outfile_name)
        print("Saving account data to %s..." % outfile_name)
        outfile.write(",provider,name,type,balance\n")
        for i in range(len(accounts)):
            account = accounts[i]
            outfile.write("%d,%s,%s,%s,%f\n" %
                          (i, account['fiLoginDisplayName'], account['accountName'], account['accountType'], account['currentBalance']))
        print("Saved account data\n")

    def get_budgets(self):
        """Get the budget data"""
        print("Getting budgets...")
        return self.mint.get_budgets()

    # TODO: format budget date output
    def save_budgets(self, budgets=None):
        """Write the budget data to a file"""
        if budgets is None:
            budgets = self.get_budgets()

        outfile_name = str("history/%s/Budgets.csv" % TODAY)
        outfile = safe_open_w(outfile_name)
        print("Saving budget data to %s..." % outfile_name)
        print(budgets, file=outfile)
        print("Saved budget data\n")

    def get_credit_score(self):
        """Get the credit score"""
        print("Getting credit score...")
        return self.mint.get_credit_score()

    def save_credit_score(self, credit_score=None):
        """Write the credit score to a file"""
        if credit_score is None:
            credit_score = self.get_credit_score()

        outfile_name = str("history/%s/CreditScore.csv" % TODAY)
        outfile = safe_open_w(outfile_name)
        print("Saving credit score to %s..." % outfile_name)
        outfile.write(str(credit_score))
        print("Saved credit score\n")

    def get_net_worth(self):
        """Get the net worth"""
        print("Getting net worth...")
        return self.mint.get_net_worth()

    def save_net_worth(self, net_worth=None):
        """Write the net worth to a file"""
        if net_worth is None:
            net_worth = self.get_net_worth()

        outfile_name = str("history/%s/NetWorth.csv" % TODAY)
        outfile = safe_open_w(outfile_name)
        print("Saving net worth to %s..." % outfile_name)
        outfile.write("%s" % net_worth)
        print("Saved net worth\n")

    def get_transactions(self):
        """Get a pandas DataFrame containing the transaction data"""
        print("Getting transactions...")
        return self.mint.get_transactions()

    def save_transactions(self, transactions=None):
        """Write the transaction data to a file"""
        if transactions is None:
            transactions = self.get_transactions()

        outfile_name = str("history/%s/Transactions.csv" % TODAY)
        print("Saving transaction data to %s..." % outfile_name)
        pd.DataFrame.to_csv(transactions, outfile_name)
        print("Saved transaction data\n")



# region Test the class

# # Login
# file = open('credentials.txt')
# username = file.readline()
# password = file.readline()
# file.close()
# mint_manager = MintManager(username, password)

# # Print full account data
# print(mint_manager.get_accounts())

# # Shutdown
# mint_manager.__del__()

# endregion