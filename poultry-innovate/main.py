import streamlit as st
from .modules import weather, news, statistics, education, financial, stakeholders, health
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from streamlit_extras.app_logo import add_logo
from streamlit_lottie import st_lottie
import requests
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Poultry-Innovate | Smart Farming Platform",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rest of your app.py code here...
# (Copy the remaining code from app.py)

if __name__ == "__main__":
    main() 