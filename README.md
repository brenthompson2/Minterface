# Minterface

A custom UI/UX for reporting and data analysis on financial data retrieved from [Intuit Mint](https://www.mint.com/).

These tools are written in Python and the [Dash](https://plot.ly/products/dash/) UI framework by Plotly.
In order to scrape the data from Mint, they use the [MintAPI by mrooney](https://github.com/mrooney/mintapi). 


### Installation

1. Download the files or clone the repo
2. Ensure python is installed by running `python --version` in terminal (Built with 3.6)

**Saved Credentials**

The application allows for the user to either type in their credentials every time or
load them from a file called `credentials.txt`. 
The format of that file is bare, with nothing but the username on the first line and the password on the second line.

```
MyFancyUsername
MySecretPassword
``` 

### Minterface GUI

TODO

### Minterface CLI

The Minterface CLI is a lightweight command line interface for getting the different pieces of mint data
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
