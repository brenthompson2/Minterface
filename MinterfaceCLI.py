from MintManager import MintManager

print("\n\n")
print("===================================================================")
print("Welcome to Minterface CLI, a command line interface for saving Intuit Mint account data to disk")
print("===================================================================")
print("\n")

# Login to mint
response = input("Do you have credentials saved in credentials.txt? (y/n): ")
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

# Save data
response = input("Save All Data? (y/n): ")
if response == 'y' or response == 'Y':
    mint.save_accounts()
    mint.save_budgets()
    mint.save_credit_score()
    mint.save_net_worth()
    mint.save_transactions()
else:
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

# Close
mint.__del__()