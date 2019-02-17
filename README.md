# Overview

Minterface is comprised of two different components used for 
analysis of financial data from [Intuit Mint](https://www.mint.com/).

- **Minterface CLI** is a lightweight command line interface for getting the different pieces of Mint data
and writing each to a file in a directory structure that allows for daily updates.
- **Minterface** is the main GUI dashboard for displaying reports that allow
for advanced data analysis on the Mint data.

These tools are written in Python and the [Dash](https://plot.ly/products/dash/) UI framework by Plotly.
In order to scrape the data from Mint, they use the [MintAPI by mrooney](https://github.com/mrooney/mintapi). 


# Installation

1. Download the files or clone the repo
2. Ensure python is installed by running `python3 --version` in terminal (Built with 3.6.5)

**Saved Credentials**

The application allows for the user to either type in their credentials every time or
load them from a file called `credentials.txt`. 
The format of that file is bare, with nothing but the username on the first line and the password on the second line.

```
MyFancyUsername
MySecretPassword
``` 

# Minterface

Minterface is the main GUI dashboard for displaying reports that allow
for advanced data analysis on the Mint data.

**As of 02/17/19 the GUI Dash app just shows a basic table of all transactions**

**Using Minterface GUI**

1. Run the application with `python Minterface.py`
1. It will ask if credentials are saved to `credentials.txt`. If not, it will prompt for them.
1. While connecting to Mint it will open a browser session, login, and wait for the account data to refresh. 
Two factor authentication is supported but will require user intervention.
1. The Dash app will launch, and for some reason the script prompts will restart.
1. After the data is re-retrieved, the GUI should be visible at the url mentioned in the terminal

# Minterface CLI

The Minterface CLI is a lightweight command line interface for getting the different pieces of Mint data
and writing each to a file in a directory structure that allows for daily updates.

```
history/
    <YYYY-MM-DD>/
        Accounts.csv
        Budgets.csv
        CreditScore.csv
        NetWorth.csv
        Transactions.csv
```

**Using Minterface CLI**

1. Run the application with `python MinterfaceCLI.py`
1. It will ask if credentials are saved to `credentials.txt`. If not, it will prompt for them.
1. While connecting to Mint it will open a browser session, login, and wait for the account data to refresh. 
Two factor authentication is supported but will require user intervention.
1. The user will then be able to specify which pieces of data to retrieve and save
