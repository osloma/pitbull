import sys, os, re
sys.path.append(".")
import streamlit as st
import pandas as pd
from data.comon import constants
from data.analysis.ark.fund_compare import ArkCompare
from data.analysis.ark.stock_extractor import StockPrice

# export PATH="$HOME/.local/bin:$PATH"


class ArkDashBoard():
    
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
        values = ArkCompare(fund).available_dates()
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
        """Populates stocks on the select box

        Args:
            c (container): streamline container where to display it
            stocks (list of strings): list containing the stocks to be shown

        Returns:
            string: stock/ticker selected
        """
        ticker = c.selectbox(
            label="Stock", options=list(stocks)
        )
        stock = ticker.split(' ')[0]
        return stock
    
    
#https://mode.com/example-gallery/python_dataframe_styling/

    def __add_table(self, c, previous_date: str, current_date: str, fund: str):
        data = ArkCompare(fund).obtain_differences(previous_date=previous_date, current_date=current_date)
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
                analysis = StockPrice(ticker, 10).get_analysis()                
                live_price = pd.DataFrame({ 'Attribute': 'Current Price', 'Value': str(StockPrice(ticker, 10).get_live_price())}, index =[0])
                data = pd.concat([live_price, analysis]).reset_index(drop = True)
                st.write(data, use_column_width=True)
            except Exception as e:
                st.write(f"I cannot get the stock for you, sorry. There us a weird exception happening as: {e}")
            
    def __show_chart(self, ticker):
        data = StockPrice(ticker, 10).get_evolution()
        with st.beta_expander("Show Charts"):
            st.line_chart(data[['adjclose', 'high', 'low', 'open']])
            st.line_chart(data['volume'])

    def __show_analyst_info(self, ticker):        
        def print_container(c, value, df):
            with c:
                st.markdown(value)
                st.write(df[value])
        
        data = StockPrice(ticker, 10).analyst_info()
        #st.write("## Analyst Information :sunglasses:")
        with st.beta_expander("Show Growth"):
            c1, c2 = st.beta_columns((1,1))
            print_container(c1, "Growth Estimates", data)
            print_container(c2, "Revenue Estimate", data)

        with st.beta_expander("Show Earnings"):
            c1, c2 = st.beta_columns((1,1))
            print_container(c1, "Earnings Estimate", data)
            print_container(c2, "Earnings History", data)

        with st.beta_expander("EPS"):
            c1, c2 = st.beta_columns((1,1))
            print_container(c1, "EPS Trend", data)
            print_container(c2, "EPS Revisions", data)
            
        

    def run(self):        
        c1, c2, c3, c4 = st.beta_columns((1,1,1,1))
        fund, previous_date, current_date = self.__add_filters(c1, c2, c3)
        r2c1, r2c2 = st.beta_columns((100,50))     
        data = self.__add_table(r2c1, previous_date=previous_date, current_date=current_date, fund=fund)
        ticker = self.__add_stock(c4, data['TICKER'])
        self.__show_analysis(r2c2, ticker)
        self.__show_chart(ticker)
        self.__show_analyst_info(ticker)
        
