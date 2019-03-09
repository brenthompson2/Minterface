from MintManager import MintManager
from MintAnalyzer import MintAnalyzer

print("\n\n")
print("===================================================================")
print("Welcome to Minterface CLI, a command line interface for saving Intuit Mint account data to disk")
print("===================================================================")
print("\n")
    
# region Login to mint & Save latest data
response = input("Retrieve Latest Intuit Mint Data? (y/n): ")
if response == 'y' or response == 'Y':
    # region Login
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
    mint = MintManager(username, password)
    mint_analyzer = MintAnalyzer(mint)
    # endregion

    # region Save data
    response = input("Save All Data? (y/n): ")
    if response == 'y' or response == 'Y':
        mint.save_accounts()
        mint.save_budgets()
        mint.save_credit_score()
        mint.save_net_worth()

        txs = mint.get_transactions()
        mint.save_transactions(txs)

        txs_per_paycheck = mint_analyzer.get_transactions_per_paycheck(txs)
        mint_analyzer.save_transactions_per_paycheck(None, txs_per_paycheck)

        spending_per_category_per_paycheck = mint_analyzer.get_spending_per_category_per_paycheck(None, txs_per_paycheck)
        mint_analyzer.save_spending_per_category_per_paycheck(spending_per_category_per_paycheck)
    else:
        response = input("Save Any Data? (y/n): ")
        if response == 'y' or response == 'Y':

            response = input("Save Account Data? (y/n): ")
            if response == 'y' or response == 'Y':
                mint.save_accounts()

            response = input("Save Budget Data? (y/n): ")
            if response == 'y' or response == 'Y':
                mint.save_budgets()

            response = input("Save Credit Score? (y/n): ")
            if response == 'y' or response == 'Y':
                mint.save_credit_score()

            response = input("Save Net Worth? (y/n): ")
            if response == 'y' or response == 'Y':
                mint.save_net_worth()

            response = input("Save Transaction Data? (y/n): ")
            if response == 'y' or response == 'Y':
                mint.save_transactions()

            response = input("Save Transactions Per Paycheck? (y/n): ")
            if response == 'y' or response == 'Y':
                mint_analyzer.save_transactions_per_paycheck()

            response = input("Save Spending Per Category Per Paycheck? (y/n): ")
            if response == 'y' or response == 'Y':
                data = mint_analyzer.get_spending_per_category_per_paycheck()
                mint_analyzer.save_spending_per_category_per_paycheck(data)
    # endregion
else:
    mint = None
    mint_analyzer = MintAnalyzer(None)
# endregion


# region Read History
response = input("Read History? (y/n): ")
if response == 'y' or response == 'Y':

    response = input("Get Account Balances Over Time? (y/n): ")
    if response == 'y' or response == 'Y':
        print(mint_analyzer.get_account_balances_over_time())
        

# endregion

# Close
if mint != None:
    mint.__del__()