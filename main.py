import matplotlib.pyplot as plt
#import alpaca_trade_api as tradeapi
from polygon import RESTClient
from backtest import backTest
import os

b = list()


def TradingSystem(prices):
    """
    This functioned is called every day with the new price data made available to it
    :param prices: this is a list of dictionaries with index zero being the oldest price data
    """
    print(prices['AAPL'][4]['t'])
    print("iteration #")
    b.append(prices['AAPL'][4]['o'])
    print(len(b))


def main():
    tickers = ['AAPL']
    back_tester = backTest('2020-01-08', '2020-05-07', 5, 100000, tickers, TradingSystem)
    back_tester.trade()
    plt.plot(b)
    plt.show()


    client = RESTClient(os.environ['APCA_API_KEY_ID'])
    response = client.stocks_equities_aggregates('AAPL', 1, 'day', '2020-01-07', '2020-01-08')



    print('end')



if __name__ == '__main__':
    main()
