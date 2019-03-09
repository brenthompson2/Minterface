import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from MintAnalyzer import MintAnalyzer

print("\n\n")
print("===================================================================")
print("Welcome to Minterface, an advanced analytical dashboard for Intuit Mint")
print("===================================================================")
print("\n")

# Initialize the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Get Account History
mint_analyzer = MintAnalyzer(None)
account_balances_over_time = mint_analyzer.get_account_balances_over_time()
account_balances_over_time_data = []
for account_key, account in account_balances_over_time.items():
    # TODO: Ensure debt accounts have negative balances
    account_balances_over_time_data.append({'x': account['dates'], 'y': account['balances'], 'type':'line', 'name':account_key})

# Draw Dash app layout
app.layout = html.Div([
    dcc.Graph(id='AccountData',
        figure = {
            'data': account_balances_over_time_data,
            'layout': {
                'title': 'Account Balances Over Time'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
