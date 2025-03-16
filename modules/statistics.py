import streamlit as st
import plotly.express as px
from data.mock_statistics import get_mock_data
import pandas as pd

def show_dashboard():
    st.header("Real-Time Poultry Statistics")
    
    col1, col2 = st.columns(2)
    
    data = get_mock_data()
    
    with col1:
        # Production trends
        fig1 = px.line(data['production'], 
                      x='month', 
                      y='value',
                      title='Monthly Production Trends')
        st.plotly_chart(fig1)
        
        # Price trends
        fig2 = px.bar(data['prices'],
                     x='region',
                     y='price',
                     title='Regional Price Distribution')
        st.plotly_chart(fig2)
    
    with col2:
        # Feed costs
        fig3 = px.pie(data['feed_costs'],
                     values='cost',
                     names='type',
                     title='Feed Cost Distribution')
        st.plotly_chart(fig3)
        
        # Key metrics
        st.subheader("Key Metrics")
        metrics = data['metrics']
        col3, col4, col5 = st.columns(3)
        col3.metric("Total Production", f"{metrics['total_production']} MT")
        col4.metric("Average Price", f"₹{metrics['avg_price']}/kg")
        col5.metric("Growth Rate", f"{metrics['growth_rate']}%")
