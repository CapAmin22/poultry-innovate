import streamlit as st
import plotly.express as px
from data.mock_statistics import get_mock_data
import pandas as pd

def show_dashboard():
    st.markdown("<h1 style='text-align: center; color: #333;'>📊 Poultry Statistics</h1>", unsafe_allow_html=True)

    data = get_mock_data()

    # Key metrics in a modern card layout
    st.markdown("""
    <style>
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    metrics = data['metrics']
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Production</h3>
            <h2>{metrics['total_production']} MT</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Average Price</h3>
            <h2>₹{metrics['avg_price']}/kg</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Growth Rate</h3>
            <h2>{metrics['growth_rate']}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive charts with modern styling
    tab1, tab2, tab3 = st.tabs(["Production", "Prices", "Feed Costs"])

    with tab1:
        fig1 = px.line(data['production'], 
                      x='month', 
                      y='value',
                      title='Monthly Production Trends')
        fig1.update_layout(
            template="plotly_white",
            margin=dict(t=30, l=10, r=10, b=10)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.bar(data['prices'],
                     x='region',
                     y='price',
                     title='Regional Price Distribution',
                     color='region')
        fig2.update_layout(
            template="plotly_white",
            margin=dict(t=30, l=10, r=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig3 = px.pie(data['feed_costs'],
                     values='cost',
                     names='type',
                     title='Feed Cost Distribution',
                     hole=0.4)
        fig3.update_layout(
            template="plotly_white",
            margin=dict(t=30, l=10, r=10, b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)