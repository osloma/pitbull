import sys, os, re
sys.path.append(".")
import streamlit as st

from selenium import webdriver

from data.analysis.ark.ark_dashboard import ArkDashBoard
from data.analysis.ark.stock_dashboard import StockOptimizerDashboard

# export PATH="$HOME/.local/bin:$PATH"

class MainDashboard():

    web_driver = webdriver.Chrome()    

    st.set_page_config(page_title="Pitbull report", page_icon=":ox:", layout="wide")

    #pages = {'ARK':ArkDashBoard,'Stock Optimizer':StockOptimizerDashboard, "Tip ranks": TipRanksAnalysis}
    pages = {'ARK':ArkDashBoard,'Stock Optimizer':StockOptimizerDashboard}

    choice = st.radio("Select analysis: ",tuple(pages.keys()))

    pages[choice]().run()