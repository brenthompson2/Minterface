import dash_core_components as dcc
import dash_html_components as html
from collections import defaultdict

class SpendingPerCategory(object):
    """
    Data object created for each category used to pair paycheck dates to the amount spent in that category
    """

    def __init__(self, category_name):
        self.category = category_name
        self.paydates = []
        self.amounts_spent = []

    def add_amount_spent_for_paycheck(self, date, amount_spent):
        """
        Adds to this collection the amount spent in this category for the specified pay date
        """
        self.paydates.append(date)
        self.amounts_spent.append(amount_spent)

    def get_graph_data(self):
        """
        Get the plotly line data for this category where the X values are the paycheck dates and the Y values are the amounts spent
        """
        return {'x': self.paydates, 'y': self.amounts_spent, 'type':'line', 'name': self.category}


class GraphSpendingPerCategoryPerPaycheck(object):
    """
    Component used to display the graph of spending per category per paycheck
    """

    def __init__(self, mint_analyzer):
        self.setup_data(mint_analyzer)
        self.layout = self.setup_layout()

    def setup_layout(self):
        """
        Initializes the layout used for displaying this component
        """
        return html.Div([
            dcc.Graph(id='GraphSpendingPerCategoryPerPaycheck',
                figure = {
                    'data': self.spending_per_category_per_paycheck_data,
                    'layout': {
                        'title': 'Spending Per Category Per Paycheck',
                        'height': '720',
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
        spending_per_paycheck_per_category = mint_analyzer.get_spending_per_paycheck_per_category()

        # Create a dictionary keyed by category where the value is the SpendingPerCategory
        spending_per_category_per_paycheck = defaultdict(SpendingPerCategory)
        for date, spending_per_category in spending_per_paycheck_per_category.items():
            categories = spending_per_category.index.tolist()
            balances = spending_per_category.values
            for i in range(0, len(categories)):
                if not categories[i] in spending_per_category_per_paycheck:
                    spending_per_category_per_paycheck[categories[i]] = SpendingPerCategory(categories[i])
                spending_per_category_per_paycheck[categories[i]].add_amount_spent_for_paycheck(date, balances[i])
        
        # Turn data into graph
        self.spending_per_category_per_paycheck_data = []
        for _, spending in spending_per_category_per_paycheck.items():
            self.spending_per_category_per_paycheck_data.append(spending.get_graph_data())

        # Hide select categories on startup
        categories_to_hide_on_startup = ['transfer', 'paycheck', 'income']
        for category_data in self.spending_per_category_per_paycheck_data:
            if category_data['name'] in categories_to_hide_on_startup:
                category_data['visible'] = "legendonly"