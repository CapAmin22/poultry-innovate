import streamlit as st
import plotly.express as px
from data.mock_statistics import get_mock_data
import pandas as pd

def show_dashboard():
    st.markdown("""
    <h1 style='text-align: center; color: #333; font-size: 2rem; margin-bottom: 2rem;'>
        📊 Market Insights
    </h1>
    """, unsafe_allow_html=True)

    data = get_mock_data()
    metrics = data['metrics']

    # Modern metric cards
    st.markdown("""
    <style>
    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ff4b4b;
        margin: 0.5rem 0;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    </style>

    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">Production</div>
            <div class="metric-value">{metrics['total_production']}MT</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Price</div>
            <div class="metric-value">₹{metrics['avg_price']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Growth</div>
            <div class="metric-value">{metrics['growth_rate']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Modern tabs for charts
    tab1, tab2, tab3 = st.tabs(["📈 Production", "📊 Prices", "🥧 Costs"])

    with tab1:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            fig1 = px.line(data['production'],
                          x='month',
                          y='value',
                          title='Monthly Production Trends')
            fig1.update_layout(
                template="plotly_white",
                margin=dict(t=30, l=10, r=10, b=10),
                height=300,
                showlegend=False,
                xaxis_title="",
                yaxis_title="Production (MT)",
                hovermode='x unified'
            )
            fig1.update_traces(line_color='#ff4b4b')
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            fig2 = px.bar(data['prices'],
                         x='region',
                         y='price',
                         title='Regional Price Distribution',
                         color_discrete_sequence=['#ff4b4b'])
            fig2.update_layout(
                template="plotly_white",
                margin=dict(t=30, l=10, r=10, b=10),
                height=300,
                xaxis_title="",
                yaxis_title="Price (₹/kg)"
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            fig3 = px.pie(data['feed_costs'],
                         values='cost',
                         names='type',
                         title='Feed Cost Distribution',
                         hole=0.6,
                         color_discrete_sequence=px.colors.sequential.Reds)
            fig3.update_layout(
                template="plotly_white",
                margin=dict(t=30, l=10, r=10, b=10),
                height=300,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)