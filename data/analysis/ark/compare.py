import pandas as pd
from os import listdir
from os.path import abspath, isfile, join
import sys, os
sys.path.append(".")
from data.comon import constants

path = os.path.abspath("download/")

def get_last_two_days(path: str) -> list:
    """
    Gets dates where ark files were downloaded as ints
    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    raw_dates = [x[x.index("-")+1:].replace(".csv", "") for x in onlyfiles]
    return list(set(map(int, raw_dates)))[-2:]

def data_per_fund(dates: list, fund: str):
    dates_path = [os.path.abspath(os.path.join(path, f"{constants.funds[fund]}-{d}.csv")) for d in dates]
    data_frames = [pd.read_csv(p) for p in dates_path]
    print(data_frames[0].merge(data_frames[1], on = "ticker", how = "right")[["date_x", "date_y", "company_x", "company_y", "shares_x", "shares_y", "weight(%)_y", "weight(%)_x"]])

if __name__ == "__main__":
    print("Starting downloading process")    
    dates = get_last_two_days(path)
    data_per_fund(dates, "Genomic")
    print("Process finished")