import os
import os.path
import pandas as pd


class MintHistoryReader(object):
    """Exposes methods for retrieving the saved Intuit Mint data"""

    def __init__(self):
        self.history_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')

    def get_accounts_over_time(self):
        """
        Get a dictionary keyed by date retrieved where the value is the snapshot of account data as a DataFrame.
        Accounts where the AccountType is credit get their value negated.
        """
        account_history = {}
        for folder_date in os.listdir(self.history_path):
            file_path = os.path.join(self.history_path, folder_date, 'Accounts.csv')
            account_snapshot = pd.DataFrame.from_csv(file_path)

            # Make credit accounts negative
            for index, row in account_snapshot.iterrows():
                if row['type'] == 'credit':
                    account_snapshot.at[index, 'balance'] = row['balance'] * -1

            account_history[folder_date] = account_snapshot
        return account_history

    def get_credit_score_over_time(self):
        """
        Get a dictionary keyed by date retrieved where the value is the credit score at that time.
        The credit score only gets added to the dictionary if it is a proper value (cast-able to an int).
        """
        credit_history = {}
        for folder_date in os.listdir(self.history_path):
            file_path = os.path.join(self.history_path, folder_date, 'CreditScore.csv')
            infile = open(file_path)
            credit_score = infile.readline()

            # Ensure the credit score is an integer
            try:
                credit_score = int(credit_score)
                credit_history[folder_date] = credit_score
            except ValueError:
                # credit score wasn't stored properly (Probably says "No credit score provided.")
                pass

        return credit_history

# Test the class
# reader = MintHistoryReader()

# accounts_over_time = reader.get_accounts_over_time()
# print(accounts_over_time)

# credit_score_over_time = reader.get_credit_score_over_time()
# print(credit_score_over_time)
