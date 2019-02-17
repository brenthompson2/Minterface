from MintManager import MintManager
import dash
import dash_table
import dash_html_components as html

print("\n\n")
print("===================================================================")
print("Welcome to Minterface, an advanced analytical dashboard for Intuit Mint")
print("===================================================================")
print("\n")

# Initialize the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

# Get transactions
transactions = mint.get_transactions()

# Draw Dash app layout
app.layout = html.Div([
    html.H1("Transactions"),

    dash_table.DataTable(
        id='Transaction Data',
        columns=[{"name": i, "id": i} for i in transactions.columns],
        data=transactions.to_dict("rows")
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
