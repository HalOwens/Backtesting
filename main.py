import matplotlib.pyplot as plt
#import alpaca_trade_api as tradeapi
from polygon import RESTClient
from backtest import backTest
import os

def TradingSystem(prices):
    """
    This functioned is called every day with the new price data made available to it
    :param prices: this is a list of dictionaries with index zero being the oldest price data
    """
    print("hello)")

def main():
    tickers = ['AAPL']
    #back_tester = backTest('2018-01-01', '2020-04-30', 60, 100000, tickers, TradingSystem)
    #back_tester.trade()
    client = RESTClient(os.environ['APCA_API_KEY_ID'])

    response = client.stocks_equities_aggregates('AAPL', 1, 'day', '2020-01-01', '2020-01-03')



    print('end')



if __name__ == '__main__':
    main()
