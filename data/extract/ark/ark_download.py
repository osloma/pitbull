import io, requests
import pandas as pd
from datetime import datetime

funds = ['ARK_INNOVATION_ETF_ARKK_HOLDINGS', 
         'ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS',
         'ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS',
         'ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS',
         'ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS']
    
custom_date_parser = lambda x: pd.datetime.strptime(x, "%m/%d/%Y")

def load_data(): 
    for f in funds:
        url = f"https://ark-funds.com/wp-content/fundsiteliterature/csv/{f}.csv"
        s = requests.get(url).content
        print(f"Downloading file {f} from {url}")
        data = pd.read_csv(io.StringIO(s.decode('utf-8')))
        data = data[data.company.notnull()]
        data["fecha"] = pd.to_datetime(data["date"], format="%m/%d/%Y")
        date = data.fecha.head().iloc[0].strftime('%Y%m%d')
        print(f"For date {date}")        
        path = f"/pitbull/download/{f}-{str(date)}.csv"
        data.to_csv(path_or_buf = path, index=False)


if __name__ == "__main__":
    print("Starting downloading process")
    load_data()
    print("Process finished")