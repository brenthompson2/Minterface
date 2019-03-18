import dash_core_components as dcc
import dash_html_components as html

class HeaderBar(object):
    """
    Component used to display the graph of account balances over time
    """

    def __init__(self):
        self.layout = self.setup_layout()

    def setup_layout(self):
        """
        Initializes the layout used for displaying this component
        """
        return html.Div([
            html.Nav(
                html.Div(
                    children=[
                        html.P('Minterface',
                                className='logo'),
                        html.Ul(
                            children=[
                                dcc.Link('Accounts Over Time', href='/accounts-over-time',
                                    className='nav-li'
                                ),
                                dcc.Link('Credit Score Over Time', href='/credit-over-time',
                                    className='nav-li'
                                ),
                                dcc.Link('Spending Per Category Per Paycheck', href='/spending-per-category-per-paycheck-data',
                                    className='nav-li'
                                ),
                            ],
                            id='nav-mobile',
                            className='nav nav-right'
                        ), 
                    ],
                    className='nav-wrapper'
                ),
                className='navbar'
            )
        ])