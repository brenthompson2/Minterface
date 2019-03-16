# Overview

Minterface is comprised of two different python applications used for 
analysis of financial data from [Intuit Mint](https://www.mint.com/).

- **Minterface CLI** is a lightweight command line interface for getting the different pieces of Mint data
and writing each to a file in a directory structure that allows for daily updates.
- **Minterface GUI** is the main GUI dashboard for displaying reports that allow
for advanced data analysis on the Mint data.

These tools are written in Python and the GUI uses the [Dash](https://plot.ly/products/dash/) UI framework by Plotly.
In order to scrape the data from Mint, they use the [MintAPI by mrooney](https://github.com/mrooney/mintapi). 

# Advanced Mint Data Analysis

The whole purpose of these applications is to add advanced analysis to the financial data retrieved from Mint. 
The applications pull down the data from Mint and store it
time-stamped in the directory structure `/history/<Date Stored>/`. 

As the user uses the applications more, the changes in data from one session to the next begin to tell a story. 
This allows `Minterface` to start showing plots and other useful graphs of the data over time.

### I) The Data

**A) Mint data from mintapi:**

- Accounts
- Budgets
- CreditScore
- NetWorth
- Transactions

**B) Minterface data:**

- **Transactions per Paycheck** = A file per paycheck containing a DataFrame of
all of the transaction data during that pay period
- **Spending per Category per Paycheck** = A file per paycheck showing
the amount spent per transaction category during that pay period

### II) Data Analysis

- **Accounts Over Time** = A line graph tracking account balances over time
- **Credit Score Over Time** = A line graph tracking credit score over time

**As of 03/11/19 nothing below here is implemented**

- **Spending per Category per Paycheck** = A pie chart showing what percentage of
spending that pay period went to which category
- **Average Spending Per Category Per Paycheck** = A pie graph showing the average percentage of
spending that went to each category for all pay periods
- **Spending Per Category Per Paycheck Over Time** = A line graph tracking how much was spent
 per transaction category per paycheck over time

# Minterface GUI

Minterface is the main GUI dashboard for displaying reports that allow
for advanced data analysis on the Mint data.

Graphs:
- Account Balances Over Time
- Credit Score Over Time

**Using Minterface GUI**

1. Run the application with `</path/to/python/> ./MinterfaceGUI.py`
1. The GUI should be visible at the url mentioned in the terminal

# Minterface CLI

The Minterface CLI is a lightweight command line interface for getting the different pieces of Mint data
and writing each to a file in a directory structure that allows for daily updates.

```
history/
    <YYYY-MM-DD>/ (The date that the data was stored)
        - Accounts.csv
        - Budgets.csv
        - CreditScore.csv
        - NetWorth.csv
        - Transactions.csv
        SpendingPerPaycheck/
            <YYYY-MM-DD>/ (The date of each paycheck)
                - Categories.csv
                - Transactions.csv
            ...
            ...
            ...
```

**Using Minterface CLI**

1. Run the application with `</path/to/python/> ./MinterfaceCLI.py`
1. It will ask if credentials are saved to `credentials.txt`. If not, it will prompt for them.
1. While connecting to Mint it will open a browser session, login, and wait for the account data to refresh. 
Two factor authentication is supported but will require user intervention.
1. The user will then be able to specify which pieces of data to retrieve and save

# Installation

1. Download the files or clone the repo
2. Ensure python is installed by running `python3 --version` in terminal (Built with 3.6.5)

### Saved Credentials

The application allows for the user to either type in their credentials every time or
load them from a file called `credentials.txt`. 
The format of that file is bare, with nothing but the username on the first line and the password on the second line.

```
MyFancyUsername
MySecretPassword
``` 