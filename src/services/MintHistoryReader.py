import errno
import os
import os.path
import pandas as pd


class MintHistoryReader(object):
    """Exposes methods for retrieving the saved Intuit Mint data"""

    def __init__(self):
        """
        Initializes the object and gets the path to the saved history data
        """
        # TODO: Get the history path from config or find something cleaner
        file_path = os.path.abspath(__file__)
        services = os.path.split(file_path)[0]
        src = os.path.split(services)[0]
        minterface = os.path.split(src)[0]
        self.history_path = os.path.join(minterface, 'history')
        while not os.path.isdir(self.history_path):
            response = input("Path to history data not found at %s. Please provide the correct path (enter 'x' to exit): " % self.history_path)
            if response == 'x' or response == 'X':
                raise FileNotFoundError("Path to history data not found at %s" % self.history_path)
            self.history_path = response

    def get_accounts_over_time(self):
        """
        Get a dictionary keyed by date retrieved where the value is the DataFrame of account data retrieved at that time.
        """
        account_history = {}
        for folder_date in os.listdir(self.history_path):
            file_path = os.path.join(self.history_path, folder_date, 'Accounts.csv')
            account_history[folder_date] = pd.read_csv(file_path)
        return account_history

    def get_credit_score_over_time(self):
        """
        Get a dictionary keyed by date retrieved where the value is the credit score retrieved at that time.
        """
        credit_history = {}
        for folder_date in os.listdir(self.history_path):
            file_path = os.path.join(self.history_path, folder_date, 'CreditScore.csv')
            infile = open(file_path)
            credit_history[folder_date] = infile.readline()
        return credit_history

# region Test the class

# print("\n===================================================================")
# print("MintHistoryReader test")
# print("===================================================================\n")

# reader = MintHistoryReader()
# print("History Path: %s" % reader.history_path)

# accounts_over_time = reader.get_accounts_over_time()
# print("\naccounts_over_time:")
# print(accounts_over_time)

# credit_score_over_time = reader.get_credit_score_over_time()
# print("\ncredit_score_over_time:")
# print(credit_score_over_time)

# endregion
