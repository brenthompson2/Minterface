from MintManager import MintManager
from MintAnalyzer import MintAnalyzer

# region Helper Functions


def login():
    """
    Login to an instance of the MintManager and return it
    """
    response = input("Are credentials saved in credentials.txt? (y/n): ")
    if response == 'y' or response == 'Y':
        file = open('credentials.txt')
        username = file.readline()
        password = file.readline()
        file.close()
    else:
        print("Please supply your Intuit Mint credentials:")
        username = input("Username: ")
        password = input("Password: ")
    return MintManager(username, password)


def save_all_data(manager, analyzer):
    """
    Save all of the data to /history for the current date, including
    accounts, budgets, credit score, net worth, transactions,
    transactions per paycheck, and spending per category per paycheck
    """
    manager.save_accounts()
    manager.save_budgets()
    manager.save_credit_score()
    manager.save_net_worth()

    txs = manager.get_transactions()
    manager.save_transactions(txs)

    txs_per_paycheck = analyzer.get_transactions_per_paycheck(txs)
    analyzer.save_transactions_per_paycheck(None, txs_per_paycheck)

    spending_per_category_per_paycheck = analyzer.get_spending_per_category_per_paycheck(None, txs_per_paycheck)
    analyzer.save_spending_per_category_per_paycheck(spending_per_category_per_paycheck)


def save_select_data(manager, analyzer):
    """
    For each piece of data, save it to a file if the user confirms that they want to
    """
    response = input("Save Account Data? (y/n): ")
    if response == 'y' or response == 'Y':
        manager.save_accounts()

    response = input("Save Budget Data? (y/n): ")
    if response == 'y' or response == 'Y':
        manager.save_budgets()

    response = input("Save Credit Score? (y/n): ")
    if response == 'y' or response == 'Y':
        manager.save_credit_score()

    response = input("Save Net Worth? (y/n): ")
    if response == 'y' or response == 'Y':
        manager.save_net_worth()

    response = input("Save Transaction Data? (y/n): ")
    if response == 'y' or response == 'Y':
        manager.save_transactions()

    response = input("Save Transactions Per Paycheck? (y/n): ")
    if response == 'y' or response == 'Y':
        analyzer.save_transactions_per_paycheck()

    response = input("Save Spending Per Category Per Paycheck? (y/n): ")
    if response == 'y' or response == 'Y':
        data = analyzer.get_spending_per_category_per_paycheck()
        analyzer.save_spending_per_category_per_paycheck(data)


def read_select_data(analyzer):
    """
    For each piece of data analysis, print it if the user confirms that they want to
    """
    response = input("Get Account Balances Over Time? (y/n): ")
    if response == 'y' or response == 'Y':
        # TODO: Save the data, create a graph off the data, or at least just print the data in a more consumable way
        print(analyzer.get_account_balances_over_time())


# endregion


print("\n\n")
print("===================================================================")
print("Welcome to Minterface CLI, a command line interface for saving Intuit Mint account data to disk")
print("===================================================================")
print("\n")

    
# region Login to mint & Save latest data
response = input("Retrieve Latest Intuit Mint Data? (y/n): ")
if response == 'y' or response == 'Y':
    mint_manager = login()
    mint_analyzer = MintAnalyzer(mint_manager)

    response = input("Save All Data? (y/n): ")
    if response == 'y' or response == 'Y':
        save_all_data(mint_manager, mint_analyzer)
    else:
        response = input("Save Any Data? (y/n): ")
        if response == 'y' or response == 'Y':
            save_select_data(mint_manager, mint_analyzer)
else:
    mint_manager = None
    mint_analyzer = MintAnalyzer(None)
# endregion

# region Read History
response = input("Read History? (y/n): ")
if response == 'y' or response == 'Y':
    read_select_data(mint_analyzer)
# endregion

# Close
if mint_manager != None:
    mint_manager.__del__()