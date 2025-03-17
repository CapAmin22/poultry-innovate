import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)

def get_market_data() -> dict:
    """Get market data from secrets or generate dummy data."""
    try:
        # Try to get market data from secrets
        market_data = st.secrets["dummy_market_data"]
        if not market_data.get("use_dummy_data", True):
            logger.info("Using real market data")
            # Implement real market data API call here
            pass
        
        # Use dummy data
        return {
            "commodities": market_data.get("commodities", {
                "corn": 7.25,
                "soybean": 14.50,
                "wheat": 6.75,
                "fishmeal": 1650.00
            }),
            "poultry": market_data.get("poultry", {
                "broiler": 2.85,
                "layer": 3.25,
                "day_old_chick": 1.50,
                "eggs": 2.25
            }),
            "trends": market_data.get("trends", {
                "feed_cost_trend": "increasing",
                "broiler_price_trend": "stable",
                "egg_price_trend": "increasing",
                "market_sentiment": "positive"
            })
        }
    except Exception as e:
        logger.error(f"Error loading market data: {str(e)}")
        return None

def generate_trend_data(base_price: float, days: int = 30) -> pd.DataFrame:
    """Generate dummy trend data for visualization."""
    dates = pd.date_range(end=datetime.now(), periods=days).tolist()
    prices = []
    current_price = base_price
    
    for _ in range(days):
        change = random.uniform(-0.05, 0.05)  # -5% to +5% daily change
        current_price *= (1 + change)
        prices.append(current_price)
    
    return pd.DataFrame({
        'date': dates,
        'price': prices
    })

def display_market_summary():
    """Display key market metrics in the dashboard."""
    try:
        market_data = get_market_data()
        if not market_data:
            st.warning("Market data temporarily unavailable")
            return
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Average Feed Price",
                f"${sum(market_data['commodities'].values()) / len(market_data['commodities']):.2f}",
                "2.1%"
            )
        
        with col2:
            st.metric(
                "Broiler Price",
                f"${market_data['poultry']['broiler']:.2f}",
                "-0.5%"
            )
        
        with col3:
            st.metric(
                "Egg Price",
                f"${market_data['poultry']['eggs']:.2f}",
                "1.8%"
            )
            
    except Exception as e:
        logger.error(f"Error displaying market summary: {str(e)}")
        st.warning("Unable to display market summary")

def show_commodity_prices():
    """Display commodity prices with interactive charts."""
    try:
        market_data = get_market_data()
        if not market_data:
            st.warning("Commodity data temporarily unavailable")
            return
            
        # Create commodity price table
        df = pd.DataFrame(list(market_data['commodities'].items()), columns=['Commodity', 'Price'])
        df['Price'] = df['Price'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(df, use_container_width=True)
        
        # Show trend chart for selected commodity
        selected_commodity = st.selectbox("Select commodity for trend analysis", list(market_data['commodities'].keys()))
        trend_data = generate_trend_data(market_data['commodities'][selected_commodity])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['date'],
            y=trend_data['price'],
            mode='lines',
            name=selected_commodity.capitalize(),
            line=dict(color='#00ff87')
        ))
        
        fig.update_layout(
            title=f"{selected_commodity.capitalize()} Price Trend",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        logger.error(f"Error displaying commodity prices: {str(e)}")
        st.error("Unable to display commodity prices")

def show_poultry_prices():
    """Display poultry product prices with interactive charts."""
    try:
        market_data = get_market_data()
        if not market_data:
            st.warning("Poultry price data temporarily unavailable")
            return
            
        # Create poultry price table
        df = pd.DataFrame(list(market_data['poultry'].items()), columns=['Product', 'Price'])
        df['Price'] = df['Price'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(df, use_container_width=True)
        
        # Show trend chart for selected product
        selected_product = st.selectbox("Select product for trend analysis", list(market_data['poultry'].keys()))
        trend_data = generate_trend_data(market_data['poultry'][selected_product])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['date'],
            y=trend_data['price'],
            mode='lines',
            name=selected_product.replace('_', ' ').title(),
            line=dict(color='#60efff')
        ))
        
        fig.update_layout(
            title=f"{selected_product.replace('_', ' ').title()} Price Trend",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        logger.error(f"Error displaying poultry prices: {str(e)}")
        st.error("Unable to display poultry prices")

def show_market_trends():
    """Display overall market trends and analysis."""
    try:
        market_data = get_market_data()
        if not market_data:
            st.warning("Market trend data temporarily unavailable")
            return
            
        trends = market_data['trends']
        
        # Display trend indicators
        cols = st.columns(4)
        
        with cols[0]:
            st.metric("Feed Cost Trend", 
                     trends['feed_cost_trend'].title(),
                     "↑" if trends['feed_cost_trend'] == "increasing" else "↓")
        
        with cols[1]:
            st.metric("Broiler Price Trend",
                     trends['broiler_price_trend'].title(),
                     "→" if trends['broiler_price_trend'] == "stable" else "↑")
        
        with cols[2]:
            st.metric("Egg Price Trend",
                     trends['egg_price_trend'].title(),
                     "↑" if trends['egg_price_trend'] == "increasing" else "↓")
        
        with cols[3]:
            st.metric("Market Sentiment",
                     trends['market_sentiment'].title(),
                     "↑" if trends['market_sentiment'] == "positive" else "↓")
        
    except Exception as e:
        logger.error(f"Error displaying market trends: {str(e)}")
        st.error("Unable to display market trends")

def show_market_module():
    """Main market analysis module display."""
    st.markdown("## Market Analysis")
    
    try:
        # Create tabs for different market views
        tab1, tab2, tab3 = st.tabs(["Commodity Prices", "Poultry Prices", "Market Trends"])
        
        with tab1:
            show_commodity_prices()
            
        with tab2:
            show_poultry_prices()
            
        with tab3:
            show_market_trends()
            
    except Exception as e:
        logger.error(f"Error in market module: {str(e)}")
        st.error("Unable to load market module. Please try again later.")

if __name__ == "__main__":
    st.set_page_config(page_title="Market Analysis", layout="wide")
    show_market_module()
