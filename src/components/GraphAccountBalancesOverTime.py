import dash_core_components as dcc
import dash_html_components as html

class GraphAccountBalancesOverTime(object):
    """
    Component used to display the graph of account balances over time
    """

    def __init__(self, mint_analyzer):
        self.setup_data(mint_analyzer)
        self.layout = self.setup_layout()

    def setup_layout(self):
        """
        Initializes the layout used for displaying this component
        """
        return html.Div([
            dcc.Graph(id='AccountData',
                figure = {
                    'data': self.account_balances_over_time_data,
                    'layout': {
                        'title': 'Account Balances Over Time',
                        'plot_bgcolor': '#2b2b2b',
                        'paper_bgcolor': '#2b2b2b',
                        'font': {
                            'color': '#fff'
                        },
                        'xaxis': {
                            'color': '#fff'
                        },
                        'yaxis': {
                            'color': '#fff'
                        }
                    }
                }
            )
        ])

    def setup_data(self, mint_analyzer):
        """
        Initializes the data used by this component
        """
        # Get Account History Graph
        account_balances_over_time = mint_analyzer.get_account_balances_over_time()
        self.account_balances_over_time_data = []
        for account_key, account in account_balances_over_time.items():
            self.account_balances_over_time_data.append({'x': account['dates'], 'y': account['balances'], 'type':'line', 'name':account_key})