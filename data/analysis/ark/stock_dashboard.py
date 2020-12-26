import sys, os, re
sys.path.append(".")

import streamlit as st
import pandas as pd
import ffn 
import numpy as np
from pylab import mpl, plt
import scipy.stats as scs
import scipy.optimize as sco
import time
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

from data.analysis.ark.stock_extractor import StockOptimizer

# https://medium.com/analytics-vidhya/constructing-a-killer-investment-portfolio-with-python-51f4f0d344be
# CAT, WMT, TSLA, APPL
class StockOptimizerDashboard():

    def __set_inputs(self):
        c1, c2, c3 = st.beta_columns((5, 1, 1))
        with c1:
            stocks = st.text_input("Enter stock names separated by comma")
            symbols = stocks.replace(" ", "").split(",")
        with c2:
            date = st.date_input("From when")
        with c3:
            calculate = st.button("Calculate")

        return symbols, date, calculate

    def __show_sharpe(self, measures):
        c1, c2, c3, c4, c5, c6, c7 = st.beta_columns((1, 1, 1, 1, 1, 1, 3))
        with c1:
            st.subheader("Annual Returns")
        with c2:
            st.subheader(f"{measures['Returns'].round(3)}%")
        with c3:
            st.subheader('Annual Volatility')
        with c4:
            st.subheader(f"{measures['Volatility'].round(3)}%")
        with c5:
            st.subheader('Sharpe')
        with c6:
            st.subheader(f"{measures['Sharpe'].round(3)}")
        with c7:
            st.text(">1 good, the bigger the better")

        

    def run(self):
        st.balloons()        
        symbols, date, calculate = self.__set_inputs()
        if calculate:
            optimum = StockOptimizer(symbols, date).estimate_portfolio_quality()
            self.__show_sharpe(optimum)