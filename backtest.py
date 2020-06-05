import os
from polygon import RESTClient
import datetime

"""
    Current Idea for flow of trades and information
    -instantiate object with settings
    -call beginTrading
    -begin trading calls the user defined trading function every day passing in the requested data
    -User makes calls to trade function
    -function attempts to execute specified trade at the current time instance
    -if succesfully executed the system returns some data 
"""


class backTest:
    """
    This class provides a structured way for accessing data and executing trades
    """
    def __init__(self, begin_date, end_date, look_back, cash, tickers, trading_func, bar_distance='day', slippage=0.02):
        """
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD
        :param beginDate: Date upon which trading will initiate
        :param endDate: Date upon which trading will end
        :param lookBack: Period in days which the system will have access to at any given time
        :param cash: Amount of liquid cash the account starts with
        :param tickers: list containing all stocks to be traded
        :param trading_func function that is called on each trading period
        :param barDistance: minute, hour, day, week etc
        :param slippage: frictional trade coefficient meant to simulate slippage
        """
        self.api_key = os.environ['APCA_API_KEY_ID']
        self.begin_date = datetime.date.fromisoformat(begin_date)
        self.end_date = datetime.date.fromisoformat(end_date)
        self.look_back = datetime.timedelta(days=look_back)
        self.cash = cash
        self.tickers = tickers
        self.trading_func = trading_func
        self.bar_distance = bar_distance
        self.slippage = slippage


    #TODO Get the system to handle trading holidays
    #Current way of approaching this is to pull 20 extra days of data and then figure out where in the data received is
    #the beginning date. Once you find that you should be able to pull the lookback period amount of data prior to that
    #date and get all the info you need
    #Concerns
    #20 is an arbitrary number that will likely not work for sufficiently long lookback periods. Aka if there are more
    #   than 20 holidays and weekends in the period its going to fail
    #While I could just make 20 into something huge that would diminish how far back I can retrieve data
    def trade(self):
        """
        This function when called begins the cycle of trading. Note that the data the system has access
        to will be the beginDate - lookback, but the first trade will be initiated as if it was done during beginDate
        The Eventual goal for this will be to implement some controls over it in tkinter
        :return:
        """
        client = RESTClient(self.api_key)
        current_date = self.begin_date
        asset = dict()
        for stock in self.tickers:
            response = client.stocks_equities_aggregates(stock, 1, self.bar_distance,
                                                         self.begin_date - datetime.timedelta(days=self.look_back)
                                                         - datetime.timedelta(days=20), self.end_date) #Currently need to find the proper date in the aggregated data
            if response.results is None: #Make sure that data is actually gotten
                    raise Exception("Unable to retrieve market data")
            asset[stock] = response.results
        offset = 0
        while current_date <= self.end_date:
            truncated_data = dict()
            for stock in self.tickers:
                truncated_data[stock] = asset[stock][offset:self.look_back.days + offset] #Creates the set of data that only includes the current lookback period
            self.trading_func(truncated_data)
            if current_date.isoweekday() == 5:
                current_date += datetime.timedelta(days=3)
            elif current_date.isoweekday() == 6:
                current_date += datetime.timedelta(days=2)
            else:
                current_date += datetime.timedelta(days=1)

