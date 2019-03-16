import dash_core_components as dcc
import dash_html_components as html

class GraphCreditScoreOverTime(object):
    """
    Component used to display the graph of credit score over time
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
                    'data': self.credit_score_over_time_data,
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
        # Setup credit score over time graph data
        credit_score_over_time = mint_analyzer.get_credit_score_over_time()
        self.credit_score_over_time_data = []
        dates = []
        credit_scores = []
        for date, credit_score in credit_score_over_time.items():
            dates.append(date)
            credit_scores.append(credit_score)
        self.credit_score_over_time_data.append({'x': dates, 'y': credit_scores, 'type':'line', 'name':'Credit Score Over Time'})