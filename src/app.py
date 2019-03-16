import dash

from services import MintAnalyzer
from components import GraphCreditScoreOverTime, GraphAccountBalancesOverTime, HeaderBar

class Application(object):
    """
    The core of the Minterface Application which includes the dash app, the dependencies, and the components
    """
    
    def __init__(self):
        """
        Initiailize the Minterface Application
        """
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        self.init_dependencies()
        self.init_components()

    def init_components(self):
        """
        Initialize the components that make up the application
        """
        self.graph_credit_score_over_time = GraphCreditScoreOverTime.GraphCreditScoreOverTime(self.mint_analyzer)
        self.graph_account_balances_over_time = GraphAccountBalancesOverTime.GraphAccountBalancesOverTime(self.mint_analyzer)
        self.headerbar = HeaderBar.HeaderBar()

    def init_dependencies(self):
        """
        Initialize the core dependencies used throughout the application
        """
        self.mint_analyzer = MintAnalyzer.MintAnalyzer(None)
