import sys, os
sys.path.append(".")
import streamlit as st
import pandas as pd
from data.comon import constants
from data.analysis.ark.compare import DataCompare

# export PATH="$HOME/.local/bin:$PATH"


class DashBoard():

    def __add_side_panel(self):
        st.sidebar.title("Pitbull Report")
        selected_metrics = st.sidebar.selectbox(
            label="Choose one of the following funds", options=list(constants.funds.keys())
        )
        return selected_metrics

    def __add_dates(self, fund: str):
        values = DataCompare(fund).available_dates()
        default_previous = values.index(values[1])
        previous_date = st.sidebar.selectbox(
            label="Previous date",
            options=values,
            index=default_previous
        )
        current_date = st.sidebar.selectbox(
            label="Current date",
            options=values
        )
        return previous_date, current_date
    
    def __add_stocks(self, fund:str):
        

#https://mode.com/example-gallery/python_dataframe_styling/

    def __add_table(self, previous_date: str, current_date: str, fund: str):
        data = DataCompare(fund).obtain_differences(previous_date=previous_date, current_date=current_date)
        st.dataframe(data.style.highlight_max(axis=0))


    def __add_title(self):
        st.markdown("""
        ### Note: 
        - I takes time to download prices as it needs to go to Yahoo Finance web service. Will improve in the future with other WS
        - Highlighted in yellow the max for weight and shares
        - SHARES(%) and WEIGHT(%) is the percentage variation from previous to current date on them
        - WEIGHT and SHARES are values for current date
        """)
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

    def __set_layout(self):
        st.set_page_config(page_title="Pitbull report", page_icon=":ox:", layout="centered")

    def run(self):        
        self.__set_layout()
        fund = self.__add_side_panel()
        previos_date, current_date = self.__add_dates(fund=fund)        
        self.__add_table(previous_date=previos_date, current_date=current_date, fund=fund)
        self.__add_title()


if __name__ == "__main__":
    DashBoard().run()