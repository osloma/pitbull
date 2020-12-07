import pandas as pd
from os import listdir
from os.path import abspath, isfile, join
import sys, os
sys.path.append(".")
from data.comon import constants

"""
Important note:
    Following code assumes that there are at least two files under folder 'download'
"""

class DataCompare():
    __path = os.path.abspath(constants.download_path)
    __colums_to_select = ["ticker", "shares", "weight_perc"]

    def __init__(self, fund):
        self.fund = fund

    def available_dates(self) -> list:
        """
        Gets dates where ark files were downloaded as ints
        """
        onlyfiles = [f for f in listdir(self.__path) if isfile(join(self.__path, f))]
        raw_dates = [x[x.index("-")+1:].replace(".csv", "") for x in onlyfiles]
        return list(set(map(int, raw_dates)))

    def __sort_df_columns(self, df):
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

        return self.__sort_df_columns(joined)

    def __differences_interday(self, data):
        """
        Calculates differences between columns shares and weight in dataframes
        """
        data["weight_per_diff"] = data["weight_perc_curr"] - data["weight_perc_prev"]    
        data["shares_diff"] = data["shares_curr"] - data["shares_prev"]
        return self.__sort_df_columns(data)

    def obtain_differences(self, previous_date, current_date):
        print("Starting downloading process")    
        df = self.__data_per_fund(previous_date, current_date, self.fund)
        return self.__differences_interday(df)


if __name__ == "__main__":
    print(DataCompare("Genomic").obtain_differences())