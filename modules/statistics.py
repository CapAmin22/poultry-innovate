import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.mock_statistics import get_mock_data

def show_dashboard():
    st.markdown("<h2>Farm Performance Dashboard</h2>", unsafe_allow_html=True)
    
    # Get mock data
    monthly_production, feed_consumption, mortality_rate, revenue_data = get_mock_data()
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="metric-value">12,500</div>
            <div class="metric-label">Total Birds</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="metric-value">{monthly_production.iloc[-1]}</div>
            <div class="metric-label">Eggs Today</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="metric-value">{mortality_rate.iloc[-1]:.1f}%</div>
            <div class="metric-label">Mortality Rate</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="metric-value">${revenue_data.iloc[-1]:,.0f}</div>
            <div class="metric-label">Monthly Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h3>Monthly Egg Production</h3>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_production.index,
            y=monthly_production.values,
            mode='lines+markers',
            name='Production',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=8, color='#4CAF50')
        ))
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, l=20, r=20, b=20),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h3>Feed Consumption Trend</h3>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=feed_consumption.index,
            y=feed_consumption.values,
            marker_color='#81C784'
        ))
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, l=20, r=20, b=20),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h3>Mortality Rate Analysis</h3>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=mortality_rate.index,
            y=mortality_rate.values,
            fill='tozeroy',
            fillcolor='rgba(76, 175, 80, 0.1)',
            line=dict(color='#4CAF50', width=2),
            mode='lines'
        ))
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, l=20, r=20, b=20),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0',
                      ticksuffix='%'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h3>Revenue Overview</h3>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=revenue_data.index,
            y=revenue_data.values,
            mode='lines+markers',
            line=dict(color='#4CAF50', width=3),
            marker=dict(
                size=8,
                color='#4CAF50',
                symbol='diamond'
            )
        ))
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, l=20, r=20, b=20),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0',
                      tickprefix='$'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Summary Cards
    st.markdown("""
    <div class="modern-card">
        <h3>Monthly Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px;">
                <h4 style="color: #2E7D32; margin: 0;">Production Efficiency</h4>
                <p style="margin: 0.5rem 0 0 0;">92% of target achieved</p>
            </div>
            <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px;">
                <h4 style="color: #2E7D32; margin: 0;">Feed Conversion</h4>
                <p style="margin: 0.5rem 0 0 0;">1.8 ratio (Good)</p>
            </div>
            <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px;">
                <h4 style="color: #2E7D32; margin: 0;">Health Status</h4>
                <p style="margin: 0.5rem 0 0 0;">Excellent</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)