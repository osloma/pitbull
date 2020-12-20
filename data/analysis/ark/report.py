import sys, os, re
sys.path.append(".")
import streamlit as st
import pandas as pd
from data.comon import constants
from data.analysis.ark.compare import DataCompare
from data.analysis.ark.stock_extractor import StockPrice

# export PATH="$HOME/.local/bin:$PATH"


class DashBoard():
    st.set_page_config(page_title="Pitbull report", page_icon=":ox:", layout="wide")

    def __add_filters(self, c1, c2, c3):
        fund = self.__add_funds(c1)
        previous_date, current_date = self.__add_dates(c2, c3, fund)        
        return fund, previous_date, current_date

    def __add_funds(self,c):
        # st.sidebar.title("Pitbull Report")
        selected_metrics = c.selectbox(
            label="Funds", options=list(constants.funds.keys())
        )
        return selected_metrics

    def __add_dates(self, cp, cc, fund: str):
        values = DataCompare(fund).available_dates()
        default_previous = values.index(values[1])
        previous_date = cp.selectbox(
            label="Previous date",
            options=values,
            index=default_previous
        )
        current_date = cc.selectbox(
            label="Current date",
            options=values
        )
        return previous_date, current_date

    def __add_stock(self, c, stocks):
        return c.selectbox(
            label="Stock", options=list(stocks)
        )
    
    
#https://mode.com/example-gallery/python_dataframe_styling/

    def __add_table(self, c, previous_date: str, current_date: str, fund: str):
        data = DataCompare(fund).obtain_differences(previous_date=previous_date, current_date=current_date)
        with c:
            c.dataframe(data.style.highlight_max(axis=0))
        return data


    def __add_title(self):
        # st.markdown("""
        # ### Note: 
        # - I takes time to download prices as it needs to go to Yahoo Finance web service. Will improve in the future with other WS
        # - Highlighted in yellow the max for weight and shares
        # - SHARES(%) and WEIGHT(%) is the percentage variation from previous to current date on them
        # - WEIGHT and SHARES are values for current date
        # """)
        st.markdown(
        f"""
            <style>
                .reportview-container .main .block-container{{                    
                    padding-top: 1rem;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-bottom: 1rem;
                    width:1700px;
                }}
                .reportview-container .main {{
                    color: black;
                    background-color: white;                    
                }}
                ul {{
                    color:green;                    
                }}
            </style>
            """,
                    unsafe_allow_html=True,
                )

    def __show_analysis(self, c, ticker):
        with c:
            try:
                stock = ticker.split(' ')[0]
                analysis = StockPrice(stock, 10).get_analysis()                
                live_price = pd.DataFrame({ 'Attribute': 'Price', 'Value': str(StockPrice(stock, 10).get_live_price())}, index =[0])
                data = pd.concat([live_price, analysis]).reset_index(drop = True)
                st.write(data, use_column_width=True)
            except Exception as e:
                st.write(f"I cannot get the stock for you, sorry. There us a weird exception happening as: {e}")

    def run(self):        
        c1, c2, c3, c4 = st.beta_columns((1,1,1,1))
        fund, previous_date, current_date = self.__add_filters(c1, c2, c3)
        r2c1, r2c2 = st.beta_columns((100,50))     
        data = self.__add_table(r2c1, previous_date=previous_date, current_date=current_date, fund=fund)
        ticker = self.__add_stock(c4, data['TICKER'])
        self.__show_analysis(r2c2, ticker)
        


if __name__ == "__main__":
    DashBoard().run()