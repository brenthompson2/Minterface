import os
import os.path
import pandas as pd


class MintHistoryReader(object):
    """Exposes methods for retrieving the saved Intuit Mint data"""

    def __init__(self):
        self.history_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')

    def get_account_history(self):
        """
        Get a dictionary keyed by date retrieved where the value is a DataFrame of account data
        """
        account_history = {}
        for folder_name in os.listdir(self.history_path):
            file_path = os.path.join(self.history_path, folder_name, 'Accounts.csv')
            account_history[folder_name] = pd.DataFrame.from_csv(file_path)
        return account_history

# Test the class
# reader = MintHistoryReader()
# accnts = reader.get_account_history()
# print(accnts)
