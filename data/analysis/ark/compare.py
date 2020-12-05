import pandas as pd
from os import listdir
from os.path import isfile, join
from pitbull.data.comon import constants


def get_days(path: str) -> list:
    """
    Gets dates where ark files were downloaded as ints
    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    raw_dates = [x[:x.index("-")+1].replace(".csv") for x in onlyfiles]
    return set(map(int, raw_dates))



if __name__ == "__main__":
    print("Starting downloading process")
    get_days("../../download")
    print("Process finished")