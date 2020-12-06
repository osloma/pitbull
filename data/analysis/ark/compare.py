import pandas as pd
from os import listdir
from os.path import abspath, isfile, join
import sys, os
sys.path.append(".")
from data.comon import constants

"""
    Following code assumes that there are at least two files under folder 'download'
"""

path = os.path.abspath("download/")
colums_to_select = ["date", "fund", "ticker", "shares", "weight_perc"]


def get_last_two_days(path: str) -> list:
    """
    Gets dates where ark files were downloaded as ints
    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    raw_dates = [x[x.index("-")+1:].replace(".csv", "") for x in onlyfiles]
    return list(set(map(int, raw_dates)))[-2:]

def sort_df_columns(df):
    """
    Sorts a dataframe on its columns based on their name alphabetically
    """
    return df[df.columns.sort_values()]

def data_per_fund(dates: list, fund: str):
    """
    Joins two days and returns a df with both dates
    """
    dates_path = [os.path.abspath(os.path.join(path, f"{constants.funds[fund]}-{d}.csv")) for d in dates]
    data_frames = [pd.read_csv(p).rename(columns={"weight(%)": "weight_perc"})[colums_to_select] for p in dates_path]
    joined = data_frames[0].merge(data_frames[-1], on = "ticker", how = "right", suffixes=("_prev", "_curr"))

    return sort_df_columns(joined)


def differences_interday(data):
    """
    Calculates differences between columns shares and weight in dataframes
    """
    data["weight_per_diff"] = data["weight_perc_curr"] - data["weight_perc_prev"]    
    data["shares_diff"] = data["shares_curr"] - data["shares_prev"]
    print(sort_df_columns(data))


if __name__ == "__main__":
    print("Starting downloading process")    
    dates = get_last_two_days(path)
    df = data_per_fund(dates, "Genomic")
    differences_interday(df)
    print("Process finished")