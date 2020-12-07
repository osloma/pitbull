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
        previous_date = st.sidebar.selectbox(
            label="Previous date",
            options=DataCompare(fund).available_dates()
        )
        current_date = st.sidebar.selectbox(
            label="Current date",
            options=DataCompare(fund).available_dates()
        )
        return previous_date, current_date

    def __add_table(self, previous_date: str, current_date: str, fund: str):
        data = DataCompare(fund).obtain_differences(previous_date=previous_date, current_date=current_date)
        st.dataframe(data)

    def run(self):        
        fund = self.__add_side_panel()
        previos_date, current_date = self.__add_dates(fund=fund)
        self.__add_table(previous_date=previos_date, current_date=current_date, fund=fund)


if __name__ == "__main__":
    DashBoard().run()