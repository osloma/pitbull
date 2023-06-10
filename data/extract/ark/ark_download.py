import io
import requests
import pandas as pd
from datetime import datetime
from data.comon import constants
import logging

    
custom_date_parser = lambda x: pd.datetime.strptime(x, "%m/%d/%Y")
logging.basicConfig(level=logging.INFO)


def load_data(): 
    """
    Downloads CSV files from the Ark Funds website and saves them to disk.

    For each fund listed in `constants.funds`, the function downloads the
    corresponding CSV file from the Ark Funds website, filters out rows where 
    the `company` field is null, converts the `date` field to a Pandas 
    `Timestamp`, and saves the resulting DataFrame to disk as a CSV file. 
    The filename of the saved file is constructed by concatenating the fund 
    symbol, a dash, and the date of the first record in the DataFrame, all
    in the format YYYYMMDD.

    Returns:
        None
    """
    for f in constants.funds.values():
        url = f"https://ark-funds.com/wp-content/fundsiteliterature/csv/{f}.csv"
        s = requests.get(url).content
        logging.info(f"Downloading file {f} from {url}")
        data = pd.read_csv(io.StringIO(s.decode('utf-8')))
        data = data[data.company.notnull()]
        data["fecha"] = pd.to_datetime(data["date"], format="%m/%d/%Y")
        date = data.fecha.head().iloc[0].strftime('%Y%m%d')        
        path = f"/pitbull/download/{f}-{str(date)}.csv"
        logging.info(f"For date {date} to {path}")
        data.to_csv(path_or_buf = path, index=False)


if __name__ == "__main__":
    """
    Entry point for the script.

    Calls the `load_data` function to download CSV files from the Ark Funds
    website and save them to disk.
    """
    logging.info("Starting downloading process")
    load_data()
    logging.info("Process finished")
