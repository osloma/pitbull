import requests
import pandas as pd
from yahoo_fin import stock_info as si

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

    def get_evolution(self):
        data = si.get_data(self.__ticker, start_date = '01/01/2018')
        print(data)
        return data

    def get_reason_for_buying_selling(self) -> str:        
        self.close_prices = self.get_evolution()
        return self.__reason()

    def analyst_info(self):
        return si.get_analysts_info(self.__ticker)

    def get_analysis(self):        
        return si.get_stats(self.__ticker).dropna(inplace=False)