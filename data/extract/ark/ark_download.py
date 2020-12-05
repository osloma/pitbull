import io, requests
import pandas as pd
from datetime import datetime
from data.comon import constants
    
custom_date_parser = lambda x: pd.datetime.strptime(x, "%m/%d/%Y")

def load_data(): 
    for f in constants.funds:
        url = f"https://ark-funds.com/wp-content/fundsiteliterature/csv/{f}.csv"
        s = requests.get(url).content
        print(f"Downloading file {f} from {url}")
        data = pd.read_csv(io.StringIO(s.decode('utf-8')))
        data = data[data.company.notnull()]
        data["fecha"] = pd.to_datetime(data["date"], format="%m/%d/%Y")
        date = data.fecha.head().iloc[0].strftime('%Y%m%d')        
        path = f"/pitbull/download/{f}-{str(date)}.csv"
        print(f"For date {date} to {path}")
        data.to_csv(path_or_buf = path, index=False)


if __name__ == "__main__":
    print("Starting downloading process")
    load_data()
    print("Process finished")