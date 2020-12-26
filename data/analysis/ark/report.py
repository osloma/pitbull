import sys, os, re
sys.path.append(".")
import streamlit as st

from data.analysis.ark.ark_dashboard import ArkDashBoard
from data.analysis.ark.stock_dashboard import StockOptimizerDashboard

# export PATH="$HOME/.local/bin:$PATH"

class MainDashboard():
    st.set_page_config(page_title="Pitbull report", page_icon=":ox:", layout="wide")

    pages = {'ARK':ArkDashBoard,'Stock Optimizer':StockOptimizerDashboard}

    choice = st.radio("Select analysis: ",tuple(pages.keys()))

    pages[choice]().run()