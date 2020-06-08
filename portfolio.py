class portfolio:
    """
    This class will track and contain the holdings of the account
    """
    def __init__(self, tickers, cash):
        """
        Initialization
        :param tickers: The list of the stocks that have the *potential* to be purchased aka the ones being tracked
        :param cash: The available purchasing power at the beginning
        """
        self.tickers = tickers
        self.cash = cash
        self.profit = 0
        self.positions =
