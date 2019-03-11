import os
import os.path
import pandas as pd


class MintHistoryReader(object):
    """Exposes methods for retrieving the saved Intuit Mint data"""

    def __init__(self):
        self.history_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')

    def get_accounts_over_time(self):
        """
        Get a dictionary keyed by date retrieved where the value is the DataFrame of account data retrieved at that time.
        """
        account_history = {}
        for folder_date in os.listdir(self.history_path):
            file_path = os.path.join(self.history_path, folder_date, 'Accounts.csv')
            account_history[folder_date] = pd.DataFrame.from_csv(file_path)
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
# reader = MintHistoryReader()

# accounts_over_time = reader.get_accounts_over_time()
# print(accounts_over_time)

# credit_score_over_time = reader.get_credit_score_over_time()
# print(credit_score_over_time)

# endregion
