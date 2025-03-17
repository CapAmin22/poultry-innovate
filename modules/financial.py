import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def get_market_data():
    """Get market data from Streamlit secrets (dummy data)."""
    try:
        return st.secrets["dummy_market_data"]
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
        return None

def display_market_summary():
    """Display market summary in the dashboard."""
    market_data = get_market_data()
    
    if not market_data:
        st.warning("Market data is temporarily unavailable")
        return

    # Create three columns for different metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Feed Price",
            f"${market_data['commodities'][0]['price']:.2f}",
            "2.5%",
            delta_color="inverse"
        )

    with col2:
        st.metric(
            "Broiler Price",
            f"${market_data['poultry_prices'][0]['price']:.2f}",
            "4.2%"
        )

    with col3:
        st.metric(
            "Egg Price",
            f"${market_data['poultry_prices'][2]['price']:.2f}",
            "1.8%"
        )

def show_market_module():
    """Display the main market analysis module."""
    st.markdown("## Market Analysis")
    
    # Get market data
    market_data = get_market_data()
    if not market_data:
        st.error("Unable to load market data")
        return

    # Create tabs for different market views
    tab1, tab2, tab3 = st.tabs(["Commodity Prices", "Poultry Prices", "Market Trends"])

    with tab1:
        show_commodity_prices(market_data['commodities'])

    with tab2:
        show_poultry_prices(market_data['poultry_prices'])

    with tab3:
        show_market_trends(market_data['market_trends'])

def show_commodity_prices(commodities):
    """Display commodity prices with interactive charts."""
    st.markdown("### Commodity Price Analysis")

    # Create a DataFrame for commodities
    df = pd.DataFrame(commodities)
    
    # Generate some historical data for visualization
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    historical_data = {}
    
    for commodity in commodities:
        base_price = commodity['price']
        # Generate realistic price variations
        prices = [base_price + random.uniform(-base_price*0.1, base_price*0.1) for _ in range(30)]
        historical_data[commodity['name']] = prices

    # Create interactive price chart
    fig = go.Figure()
    
    for commodity_name, prices in historical_data.items():
        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            name=commodity_name,
            mode='lines+markers'
        ))

    fig.update_layout(
        title="30-Day Price Trends",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display current prices in a table
    st.markdown("### Current Prices")
    st.dataframe(df, hide_index=True)

def show_poultry_prices(prices):
    """Display poultry prices with trends."""
    st.markdown("### Poultry Market Prices")

    # Create a DataFrame for poultry prices
    df = pd.DataFrame(prices)
    
    # Generate historical data for visualization
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    historical_data = {}
    
    for item in prices:
        base_price = item['price']
        # Generate realistic price variations
        price_data = [base_price + random.uniform(-base_price*0.1, base_price*0.1) for _ in range(30)]
        historical_data[item['type']] = price_data

    # Create interactive chart
    fig = go.Figure()
    
    for product, prices in historical_data.items():
        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            name=product,
            mode='lines+markers'
        ))

    fig.update_layout(
        title="30-Day Poultry Price Trends",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display current prices
    st.markdown("### Current Market Rates")
    st.dataframe(df, hide_index=True)

def show_market_trends(trends):
    """Display market trends and forecasts."""
    st.markdown("### Market Trends and Forecasts")

    # Create a DataFrame for trends
    df = pd.DataFrame(trends)
    
    # Display trends in a styled table
    st.dataframe(
        df.style.apply(lambda x: ['background-color: #f0f2f6']*len(x) if x.name % 2 else ['background-color: white']*len(x), axis=1),
        hide_index=True
    )

    # Add market insights
    st.markdown("### Market Insights")
    st.info("""
    🔍 **Current Market Analysis**
    - Demand continues to show strong growth in the poultry sector
    - Supply chain efficiency has improved in recent months
    - Price trends indicate a favorable market for producers
    """)

    # Add recommendations
    st.markdown("### Recommendations")
    st.success("""
    📈 **Strategic Actions**
    1. Consider stocking up on feed at current prices
    2. Monitor supply chain for potential disruptions
    3. Plan for increased production to meet rising demand
    """)

if __name__ == "__main__":
    st.set_page_config(page_title="Market Analysis", layout="wide")
    show_market_module()
