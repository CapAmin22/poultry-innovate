import streamlit as st
from modules import weather, news, collaboration
import os
from streamlit_option_menu import option_menu
from streamlit_extras.app_logo import add_logo
from streamlit_lottie import st_lottie
import requests
import json
import logging
from datetime import datetime
import sys
from pathlib import Path

# Configure basic logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
logger.info("Application starting up")

# Try to import logo component with fallback
try:
    from streamlit_extras.app_logo import add_logo
    HAS_LOGO_COMPONENT = True
except ImportError:
    logger.warning("Could not import logo component, will use text header instead")
    HAS_LOGO_COMPONENT = False

# Initialize configuration from Streamlit secrets
def get_secret(key, default=None):
    """Safely get a secret from Streamlit secrets."""
    try:
        return st.secrets[key]
    except KeyError:
        if default is not None:
            return default
        logger.warning(f"Missing secret: {key}")
        return None

# Load configuration
try:
    # API Keys - with fallbacks for local development
    OPENWEATHER_API_KEY = get_secret("openweather_api_key")
    NEWS_API_KEY = get_secret("news_api_key")
    
    # API URLs - with fallbacks
    WEATHER_API_URL = get_secret("api_urls", {}).get("weather", "https://api.openweathermap.org/data/2.5")
    NEWS_API_URL = get_secret("api_urls", {}).get("news", "https://newsapi.org/v2")
    MARKET_API_URL = get_secret("api_urls", {}).get("market")
    
    # Application Settings
    DEBUG = get_secret("settings")["debug"]
    ENVIRONMENT = get_secret("settings")["environment"]
    CACHE_TIMEOUT = get_secret("settings")["cache_timeout"]
    
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    # Don't stop the app, continue with reduced functionality

def load_lottie_url(url: str) -> dict | None:
    """
    Load a Lottie animation from a URL.
    
    Args:
        url (str): The URL of the Lottie animation JSON file
        
    Returns:
        dict | None: The Lottie animation as a dictionary if successful, None otherwise
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"Error loading Lottie animation from {url}: {str(e)}")
        return None

# Load animations
lottie_chicken = load_lottie_url("https://lottie.host/58194a35-654d-4e9d-9d2d-4296f8c55938/KpvLxvEGVr.json")
lottie_weather = load_lottie_url("https://lottie.host/c022a6f8-2c28-46cc-9769-27c9c3c8f27c/6woQQX7Bhs.json")

# Page configuration
st.set_page_config(
    page_title="22Poultry | Smart Farming Platform",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add Font Awesome
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# Modern mobile-first CSS with enhanced design
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, -apple-system, sans-serif;
        color: #e2e8f0;
    }

    /* Typography Improvements */
    h1 {
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        background: linear-gradient(120deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        background: linear-gradient(120deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h3 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    p {
        color: #e2e8f0;
        line-height: 1.8;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Modern Card Design */
    .modern-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(148, 163, 184, 0.2);
        background: rgba(30, 41, 59, 0.8);
    }

    /* Dashboard Cards */
    .dashboard-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s ease;
    }

    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        border-color: rgba(148, 163, 184, 0.2);
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid rgba(148, 163, 184, 0.2);
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
        font-size: 1rem;
        color: #e2e8f0;
        background: rgba(30, 41, 59, 0.7);
    }

    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        background: rgba(30, 41, 59, 0.9);
    }

    /* Buttons */
    .stButton button {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        color: #ffffff;
        border: none;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
        opacity: 0.95;
    }

    /* Navigation Menu */
    .nav-link {
        border-radius: 12px !important;
        margin: 4px 0 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        color: #e2e8f0 !important;
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
    }

    .nav-link:hover {
        background: rgba(56, 189, 248, 0.1) !important;
        color: #ffffff !important;
        border-color: rgba(56, 189, 248, 0.2) !important;
    }

    .nav-link.active {
        background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
    }

    /* Metrics and KPIs */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.2);
        background: rgba(30, 41, 59, 0.8);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 500;
    }

    /* Notifications */
    .notification {
        background: rgba(30, 41, 59, 0.7);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #38bdf8;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .notification:hover {
        transform: translateX(4px);
        background: rgba(30, 41, 59, 0.8);
    }

    /* News Cards */
    .news-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .news-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.2);
        background: rgba(30, 41, 59, 0.8);
    }

    .news-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .news-meta {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 1rem;
    }

    /* Weather Widget */
    .weather-widget {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .weather-widget:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.2);
        background: rgba(30, 41, 59, 0.8);
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-bottom: 1rem;}
</style>
""", unsafe_allow_html=True)

def main() -> None:
    """
    Main application function that sets up the Streamlit interface and handles navigation.
    Manages the main layout, navigation, and different sections of the application.
    """
    try:
        # Add logo and header with animation
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if lottie_chicken:
                    st_lottie(lottie_chicken, height=100, key="logo")
                else:
                    st.markdown("🐔")
            with col2:
                st.markdown("""
                    <div style='text-align: center; padding: 1rem 0;'>
                        <h1 style='margin: 0; font-size: 3.8rem;'>22Poultry</h1>
                        <p style='color: #94a3b8; margin-top: 0.5rem; font-size: 1.2rem;'>Smart Farming Platform</p>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                if lottie_weather:
                    st_lottie(lottie_weather, height=100, key="weather_anim")

        # Initialize session state
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
            
        # Display any pending notifications
        display_notifications()
        
        # Navigation menu with improved styling
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Weather", "News", "Collaboration"],
            icons=["house-fill", "cloud-sun-fill", "newspaper", "people-fill"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0.5rem", "background-color": "rgba(30, 41, 59, 0.3)", "border-radius": "12px", "margin": "1rem 0"},
                "icon": {"color": "#38bdf8", "font-size": "1rem"},
                "nav-link": {
                    "text-align": "center",
                    "margin": "0.2rem",
                    "padding": "1rem",
                    "border-radius": "8px",
                    "--hover-color": "rgba(56, 189, 248, 0.1)",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #38bdf8, #818cf8)",
                    "color": "white",
                },
            }
        )
        
        # Display selected section
        if selected == "Dashboard":
            display_dashboard()
        elif selected == "Weather":
            weather.show_weather()
        elif selected == "News":
            news.show_news()
        elif selected == "Collaboration":
            collaboration.show_collaboration_module()
            
    except Exception as e:
        logger.error(f"Error in main application: {e}")
        st.error("An error occurred while loading the application. Please try refreshing the page.")

def display_dashboard() -> None:
    """
    Display the main dashboard with integrated market analysis and insights.
    """
    try:
        # Dashboard Header with Animation
        st.markdown("""
            <div style='display: flex; align-items: center; margin-bottom: 2rem; background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(148, 163, 184, 0.1);'>
                <div>
                    <h1 style='margin: 0; font-size: 2.8rem;'>Dashboard Overview</h1>
                    <p style='color: #94a3b8; margin-top: 0.5rem;'>Monitor your farm's performance and insights</p>
                </div>
                <div style='margin-left: auto; background: rgba(56, 189, 248, 0.1); padding: 0.75rem 1.5rem; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.2);'>
                    <span style='color: #38bdf8; font-size: 1.1rem;'>Last updated: {}</span>
                </div>
            </div>
        """.format(datetime.now().strftime("%B %d, %Y %H:%M")), unsafe_allow_html=True)
        
        # Quick Stats Row with Icons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
                <div class='metric-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <i class="fas fa-temperature-high" style='color: #38bdf8; font-size: 1.5rem; margin-right: 0.5rem;'></i>
                    </div>
                    <div class='metric-value'>24.5°C</div>
                    <div class='metric-label'>Average Temperature</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='metric-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <i class="fas fa-tint" style='color: #38bdf8; font-size: 1.5rem; margin-right: 0.5rem;'></i>
                    </div>
                    <div class='metric-value'>78%</div>
                    <div class='metric-label'>Humidity Level</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class='metric-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <i class="fas fa-check-circle" style='color: #38bdf8; font-size: 1.5rem; margin-right: 0.5rem;'></i>
                    </div>
                    <div class='metric-value'>Optimal</div>
                    <div class='metric-label'>Farm Conditions</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class='metric-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <i class="fas fa-bell" style='color: #38bdf8; font-size: 1.5rem; margin-right: 0.5rem;'></i>
                    </div>
                    <div class='metric-value'>3</div>
                    <div class='metric-label'>Active Alerts</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Main Content with Enhanced Layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Weather Forecast with Animation
            st.markdown("""
                <div class='dashboard-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>Weather Forecast</h3>
                        <div style='margin-left: auto;'>
                            <i class="fas fa-sync-alt" style='color: #38bdf8; cursor: pointer;'></i>
                        </div>
                    </div>
                    <div class='weather-widget'>
            """, unsafe_allow_html=True)
            weather.display_weather_widget()
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Market Analysis with Enhanced Visuals
            st.markdown("""
                <div class='dashboard-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>Market Insights</h3>
                        <div style='margin-left: auto;'>
                            <i class="fas fa-chart-line" style='color: #38bdf8;'></i>
                        </div>
                    </div>
                    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
            """, unsafe_allow_html=True)
            
            st.metric(
                "Market Sentiment",
                "Positive",
                "2.1%",
                help="Overall market sentiment based on recent trends"
            )
            st.metric(
                "Supply Status",
                "Stable",
                "0.5%",
                help="Current supply chain status"
            )
            st.metric(
                "Demand Trend",
                "Growing",
                "3.2%",
                help="Current demand trend in the market"
            )
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Recent Updates with Enhanced Design
            st.markdown("""
                <div class='dashboard-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>Recent Updates</h3>
                        <div style='margin-left: auto;'>
                            <i class="fas fa-users" style='color: #38bdf8;'></i>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            collaboration.init_session_state()
            recent_posts = st.session_state.posts[:3]
            for post in recent_posts:
                collaboration.show_post(post)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Active Alerts with Enhanced Styling
            st.markdown("""
                <div style='background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>Active Alerts</h3>
                        <div style='margin-left: auto;'>
                            <i class="fas fa-bell" style='color: #38bdf8;'></i>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            if st.session_state.notifications:
                for notification in st.session_state.notifications:
                    st.markdown(f"""
                        <div class="notification">
                            <strong>{notification['title']}</strong><br>
                            <p style='margin: 0.5rem 0 0 0; color: #94a3b8;'>{notification['message']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No new notifications")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Latest News with Enhanced Design
            st.markdown("""
                <div style='background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 16px;'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='margin: 0;'>Latest News</h3>
                        <div style='margin-left: auto;'>
                            <i class="fas fa-newspaper" style='color: #38bdf8;'></i>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            news.show_news_summary()
            st.markdown("</div>", unsafe_allow_html=True)
            
    except Exception as e:
        logger.error(f"Error in dashboard display: {str(e)}")
        st.error("Unable to load dashboard components. Please refresh the page.")

def display_notifications() -> None:
    """Display recent notifications and alerts in the dashboard."""
    try:
        with st.container():
            st.markdown("### Recent Notifications")
            if st.session_state.notifications:
                for notification in st.session_state.notifications:
                    st.markdown(f"""
                        <div class="notification">
                            <strong>{notification['title']}</strong><br>
                            {notification['message']}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No new notifications")
    except Exception as e:
        logger.error(f"Error displaying notifications: {str(e)}")
        st.warning("Unable to load notifications")

if __name__ == "__main__":
    try:
        # Add a health check endpoint
        if "healthz" in st.query_params:
            st.success("Health check passed")
        else:
            main()
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}")
        st.error("Critical error: Unable to start the application. Please contact support.")