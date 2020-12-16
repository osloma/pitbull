import pandas as pd
import numpy as np
from os import listdir
from os.path import abspath, isfile, join

from data.analysis.ark.stock_extractor import StocksPrice

import sys, os
sys.path.append(".")
from data.comon import constants

"""
Important note:
    Following code assumes that there are at least two files under folder 'download'
"""

class DataCompare():
    __path = os.path.abspath(constants.download_path)
    __colums_to_select = ["ticker", "company", "shares", "weight_perc"]

    def __init__(self, fund):
        self.fund = fund

    def available_dates(self) -> list:
        """
        Gets dates where ark files were downloaded as ints
        """
        onlyfiles = [f for f in listdir(self.__path) if isfile(join(self.__path, f))]
        raw_dates = [x[x.index("-")+1:].replace(".csv", "") for x in onlyfiles]
        

        return sorted(list(set(map(int, raw_dates))), reverse=True)

    def __sort_df_columns_alpha(self, df):
        """
        Sorts a dataframe on its columns based on their name alphabetically
        """
        return df[df.columns.sort_values()]

    def __data_per_fund(self, previous_date: str, current_date: str, fund: str):
        """
        Joins two days and returns a df with both dates
        """
        get_path = lambda date: os.path.abspath(os.path.join(self.__path, f"{constants.funds[fund]}-{date}.csv"))
        get_data = lambda path: pd.read_csv(path).rename(columns={"weight(%)": "weight_perc"})[self.__colums_to_select] 
        
        previous_data = get_data(get_path(previous_date))
        current_data = get_data(get_path(current_date))

        joined = previous_data.merge(current_data, on = "ticker", how = "right", suffixes=("_prev", "_curr"))

        return self.__sort_df_columns_alpha(joined)

    def __differences_interday(self, data):
        """
        Calculates differences between columns shares and weight in dataframes
        """
        data["weight_perc_diff"] = data["weight_perc_curr"] - data["weight_perc_prev"]    
        data["shares_diff"] = (data["shares_curr"] - data["shares_prev"])/data["shares_prev"]*100
        prices = self.__get_stocks_price(data)
        data = data.merge(prices, on = 'ticker', how = "left")

        col_rename = {'shares_diff': 'SHARES(%)', 'ticker': 'TICKER', 'shares_curr': 'SHARES', 
            'weight_perc_curr': 'WEIGHT', 'weight_perc_diff': 'WEIGHT(%)', 'company_curr': 'COMPANY', 'price': 'PRICE', 'reason': 'REASON'}
        col_output = ['COMPANY','TICKER', 'SHARES(%)', 'WEIGHT(%)', 'PRICE', 'WEIGHT', 'SHARES', 'REASON']

        return self.__sort_df_columns_alpha(data).rename(columns=col_rename)[col_output]

    def __get_stocks_price(self, df):
        """
        Obtains real time stock prices 
        """
        tickers = df['ticker'].tolist()
        print(tickers)
        prices = pd.DataFrame(columns = ['ticker', 'price', 'reason'])
        for t in tickers:
            if t == t:
                ticker = t.split(' ')[0]
                stock = StocksPrice(ticker=ticker, n=20)
                live_price = stock.get_live_price()
                reason = stock.get_reason_for_buying_selling()
                prices = prices.append({'ticker': t, 'price': live_price, 'reason': reason}, ignore_index=True)
        return prices


    def obtain_differences(self, previous_date, current_date):
        print("Starting downloading process")    
        df = self.__data_per_fund(previous_date, current_date, self.fund)
        return self.__differences_interday(df)


if __name__ == "__main__":
    print(DataCompare("Genomic").obtain_differences())