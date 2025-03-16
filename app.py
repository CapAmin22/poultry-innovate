import streamlit as st
from modules import weather, news, statistics, education, financial, stakeholders
import pandas as pd

st.set_page_config(
    page_title="Indian Poultry Stakeholder Platform",
    page_icon="🐔",
    layout="wide"
)

def main():
    st.title("Indian Poultry Stakeholder Platform")
    
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Education", "Weather", "Financial Assistance", 
         "Stakeholder Directory", "Industry News"]
    )
    
    if menu == "Dashboard":
        statistics.show_dashboard()
    
    elif menu == "Education":
        education.show_content()
    
    elif menu == "Weather":
        weather.show_forecast()
    
    elif menu == "Financial Assistance":
        financial.show_assistance()
    
    elif menu == "Stakeholder Directory":
        stakeholders.show_directory()
    
    elif menu == "Industry News":
        news.show_news()

if __name__ == "__main__":
    main()
