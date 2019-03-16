import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from services import MintAnalyzer
from app import Application

# Initialize the Dash app
minterface = Application()
mint_analyzer = minterface.mint_analyzer

# region Layout

minterface.app.layout = html.Div([
    # URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # Navbar
    html.Div(id='header-component'),

    # Content
    html.Div(id='page-content',
            className='content')
])

# endregion

# region Callbacks

@minterface.app.callback([
    dash.dependencies.Output('header-component', 'children'),
    dash.dependencies.Output('page-content', 'children')],
    [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    header_component = minterface.headerbar.layout
    if pathname == '/credit-over-time':
        page_content = minterface.graph_credit_score_over_time.layout
    else:
        page_content = minterface.graph_account_balances_over_time.layout
    return header_component, page_content

# endregion

if __name__ == '__main__':
    minterface.app.run_server(debug=True)