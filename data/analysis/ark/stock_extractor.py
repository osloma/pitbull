import requests
import pandas as pd
from yahoo_fin import stock_info as si
import ffn 
import numpy as np
import scipy.stats as scs
import scipy.optimize as sco
import time

class StockPrice():
    def __init__(self, ticker: str, n: int) -> None:
        self.__ticker = ticker
        self.__n = n

    def get_live_price(self) -> float:        
        self.__live_price = si.get_live_price(self.__ticker)
        return self.__live_price

    def __moving_avg(self, prices):
        return prices.rolling(window=self.__n).mean().iloc[self.__n-1:].values[-1]

    # si.get_stats('tsla')
    # https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/

    
    def __reason(self):
        """
        Compares live price with moving average
        """
        print("Formula")
        print(self.__moving_avg(self.close_prices))
        print(self.__live_price)
        print(self.__moving_avg(self.close_prices) > self.__live_price)
        reason = {'GROWING': self.__moving_avg(self.close_prices) > self.__live_price, 
                'LOWERING': self.__moving_avg(self.close_prices) < self.__live_price}

        return [x for (x,y) in reason.items() if y][0]

    def get_evolution(self, start_date = '01/01/2018' ):
        data = si.get_data(self.__ticker, start_date = start_date)
        return data

    def get_reason_for_buying_selling(self) -> str:        
        self.close_prices = self.get_evolution()
        return self.__reason()

    def analyst_info(self):
        return si.get_analysts_info(self.__ticker)

    def get_analysis(self):        
        return si.get_stats(self.__ticker).dropna(inplace=False)


class StockOptimizer():

    def __init__(self, stocks, start_date):
        self.__stocks = stocks
        self.__start_date = start_date
        self.__returns = self.__fetch_stock_returns(self.__stocks)

    def __fetch_stock_returns(self, symbols):   
        prices = ffn.get(symbols, start='2010-10-10')
        #Calculate Daily Returns
        return np.log(prices / prices.shift(1))

    def portfolio_returns(self, weights):        
        return np.sum(self.__returns.mean() * weights) * 252

    def portfolio_volume(self, weights):        
        return np.sqrt(np.dot(weights.T, np.dot(self.__returns.cov() * 252, weights)))

    def min_func_sharpe(self, weights):
        """function that allows us to assess the strength of our portfolio. A value of 1 or higher is considered good

        Args:
            weights (list): for each of the symbol

        Returns:
            double: if greater than 1, stock is good
        """
        returns = self.portfolio_returns(weights)
        volumes = self.portfolio_volume(weights)
        return -(returns)/(volumes)

    def estimate_portfolio_quality(self):        
        number_of_assets = len(self.__stocks)
        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)-1})
        bounds = tuple((0,1) for x in range(number_of_assets))
        eweights = np.array(number_of_assets * [1. / number_of_assets,])
        model = sco.minimize(self.min_func_sharpe, eweights, method='SLSQP', bounds=bounds, constraints=cons)
        returns = self.portfolio_returns(model['x'])*100
        volatility = self.portfolio_volume(model['x'])*100
        return {'Returns': returns,
                "Volatility": volatility,
                'Sharpe': returns/volatility
        }