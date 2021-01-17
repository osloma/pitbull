import pandas as pd
import numpy as np
import math
from os import listdir
from os.path import abspath, isfile, join

import sys, os
sys.path.append(".")
from data.comon import constants

from data.analysis.ark.stock_extractor import StockPrice
from data.performance import concurrency

"""
Important note:
    Following code assumes that there are at least two files under folder 'download'
"""

class ArkCompare():
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

        col_rename = {'shares_diff': 'SHARES(%)', 'ticker': 'TICKER', 'shares_curr': 'SHARES', 
            'weight_perc_curr': 'WEIGHT', 'weight_perc_diff': 'WEIGHT(%)', 'company_curr': 'COMPANY'}
        col_output = ['COMPANY','TICKER', 'SHARES(%)', 'WEIGHT(%)', 'WEIGHT', 'SHARES']

        return self.__sort_df_columns_alpha(data).rename(columns=col_rename)[col_output]

    def obtain_differences(self, previous_date, current_date):        
        df = self.__data_per_fund(previous_date, current_date, self.fund)
        return self.__differences_interday(df)


class ArkExtractor():
    __path = os.path.abspath(constants.download_path)

    def get_all_tickers(self):
        tickers = pd.Series(dtype="string")
        for file in os.listdir(self.__path):            
            t = pd.read_csv(os.path.join(self.__path, file))['ticker']
            tickers = pd.concat([tickers, t]).drop_duplicates()
        self.__tickers = tickers.unique()
        return self.__tickers

#https://medium.com/analytics-vidhya/python-decorator-to-parallelize-any-function-23e5036fb6a

    def __get_analyst_info(self, stock):
        def clean(value):            
            result = str(value).replace('%', '').replace(',', '').split('.')[0]
            try:
                a = result if result.isnumeric() else 0
                result = int(a)
            except:
                result = f"Not a number {result}"
            return result
        output = StockPrice(stock, 10).analyst_info()
        next_quarter_growth = clean(output["Growth Estimates"][stock].iloc[1])
        next_year_growth = clean(output["Growth Estimates"][stock].iloc[3])
        return {'ticker': stock, 'next_quarter_growth': next_quarter_growth, 'next_year_growth': next_year_growth}

    def get_best_growers(self):
        tickers = [ticker.split(' ')[0] for ticker in self.__tickers if ticker == ticker and (not ticker.isnumeric())]

        from itertools import islice

        # https://www.geeksforgeeks.org/python-split-a-list-into-sublists-of-given-lengths/

        growth = pd.DataFrame(columns = ['ticker', 'next_quarter_growth', 'next_year_growth'])
        growth = growth.astype(dtype={'ticker': str, 'next_quarter_growth': int, 'next_year_growth': int}) 
        for i in range(1,len(tickers)-30, 10):
            estimates = concurrency.make_parallel(self.__get_analyst_info)(tickers[i:i+10])
            growth = growth.append(estimates, ignore_index=True)
        
        return growth.sort_values(by="next_quarter_growth", ascending=False)


if __name__ == "__main__":
    print(DataCompare("Genomic").obtain_differences())