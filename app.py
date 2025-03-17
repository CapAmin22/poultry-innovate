import streamlit as st
from modules import weather, news, statistics, education, financial, stakeholders, health
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
lottie_chicken = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_GofK09iPAE.json")
lottie_weather = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_KUFdS6.json")

# Page configuration
st.set_page_config(
    page_title="22Poultry | Smart Farming Platform",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern mobile-first CSS with enhanced design
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #1a1c2b 0%, #2d3047 100%);
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        color: #ffffff;
    }

    /* Typography Improvements */
    h1 {
        color: #ffffff;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(120deg, #00ff87, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    h3 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    p {
        color: #ffffff;
        line-height: 1.8;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Modern Card Design */
    .modern-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        border-color: rgba(255,255,255,0.3);
        background: rgba(255, 255, 255, 0.15);
    }

    /* Dashboard Stats Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
    }

    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.3);
        background: rgba(255, 255, 255, 0.15);
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox select {
        border-radius: 12px;
        border: 2px solid rgba(37, 99, 235, 0.2);
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
        font-size: 1rem;
        color: #1e293b;
        background: white;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
    }

    /* Buttons */
    .stButton button {
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        background: #2563eb;
        color: white;
        border: none;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        background: #1d4ed8;
    }

    /* Navigation Menu */
    .nav-link {
        border-radius: 12px !important;
        margin: 4px 0 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .nav-link:hover {
        background: rgba(0, 255, 135, 0.2) !important;
        color: #ffffff !important;
        border-color: rgba(0, 255, 135, 0.3) !important;
    }

    .nav-link.active {
        background: linear-gradient(120deg, #00ff87, #60efff) !important;
        color: #1a1c2b !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(0, 255, 135, 0.3) !important;
    }

    /* Metrics and KPIs */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        background: linear-gradient(120deg, #00ff87, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 1.1rem;
        color: #ffffff;
        margin-top: 0.5rem;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    /* Charts and Graphs */
    .plot-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* Tables */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .dataframe th {
        background: #f1f5f9;
        padding: 1rem;
        font-weight: 600;
        color: #334155;
    }

    .dataframe td {
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
        color: #475569;
    }

    /* Notifications */
    .notification {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #00ff87;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        color: #ffffff;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
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
        # Add logo or header
        with st.container():
            col1, col2 = st.columns([1, 5])
            with col1:
                if HAS_LOGO_COMPONENT:
                    try:
                        add_logo("generated-icon.png", height=80)
                    except Exception as e:
                        logger.warning(f"Could not load logo: {e}")
                        st.markdown("🐔")
                else:
                    st.markdown("🐔")
            with col2:
                st.markdown("<h1 style='margin-top: 0.5rem;'>22Poultry</h1>", unsafe_allow_html=True)

        # Initialize session state
        if 'user_location' not in st.session_state:
            st.session_state.user_location = None
            logger.info("Initialized user_location in session state")
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
            logger.info("Initialized notifications in session state")

        # Modern Navigation
        try:
            selected = option_menu(
                menu_title=None,
                options=["Dashboard", "Health", "Weather", "Market", "Education", "Network", "News"],
                icons=["graph-up", "heart-pulse", "cloud-sun", "currency-dollar", "book", "people", "newspaper"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {
                        "padding": "0.5rem",
                        "background-color": "transparent",
                        "border-radius": "15px",
                        "margin-bottom": "2rem"
                    },
                    "icon": {"color": "#2563eb", "font-size": "1.1rem"},
                    "nav-link": {
                        "font-size": "1rem",
                        "text-align": "center",
                        "padding": "1rem",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                }
            )
        except Exception as e:
            logger.error(f"Error in navigation menu: {e}")
            selected = "Dashboard"  # Fallback to dashboard

        # Handle navigation selection with error handling for each module
        try:
            if selected == "Dashboard":
                display_dashboard()
            elif selected == "Health":
                health.show_health_module()
            elif selected == "Weather":
                weather.show_weather_module()
            elif selected == "Market":
                financial.show_market_module()
            elif selected == "Education":
                education.show_education_module()
            elif selected == "Network":
                stakeholders.show_network_module()
            elif selected == "News":
                news.show_news_module()
        except Exception as e:
            logger.error(f"Error in module {selected}: {str(e)}")
            st.error(f"An error occurred while loading the {selected} module. Please try again later.")
            # Display a basic fallback UI
            st.markdown("### Module Temporarily Unavailable")
            st.markdown("We're experiencing technical difficulties. Please try:")
            st.markdown("1. Refreshing the page")
            st.markdown("2. Selecting a different module")
            st.markdown("3. Checking back later")

    except Exception as e:
        logger.error(f"Critical error in main application: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page or contact support.")
        # Provide basic functionality even in case of errors
        st.markdown("### Emergency Mode")
        st.markdown("The application is running in a reduced functionality mode.")

def display_dashboard() -> None:
    """
    Display the main dashboard with key metrics and overview information.
    Includes weather summary, health alerts, market trends, and recent news.
    """
    try:
        st.markdown("## Dashboard Overview")
        
        # Create dashboard layout with error handling for each section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                display_weather_summary()
            except Exception as e:
                logger.error(f"Error in weather summary: {e}")
                st.warning("Weather information temporarily unavailable")
        
        with col2:
            try:
                display_health_metrics()
            except Exception as e:
                logger.error(f"Error in health metrics: {e}")
                st.warning("Health metrics temporarily unavailable")
        
        with col3:
            try:
                display_market_trends()
            except Exception as e:
                logger.error(f"Error in market trends: {e}")
                st.warning("Market trends temporarily unavailable")
        
        # Display notifications with error handling
        try:
            display_notifications()
        except Exception as e:
            logger.error(f"Error displaying notifications: {e}")
            st.warning("Notifications temporarily unavailable")
            
    except Exception as e:
        logger.error(f"Error in dashboard display: {str(e)}")
        st.error("Unable to load dashboard components. Please refresh the page.")

def display_weather_summary() -> None:
    """Display a summary of current weather conditions and forecasts."""
    try:
        with st.container():
            st.markdown("### Weather Summary")
            weather.display_weather_widget()
    except Exception as e:
        logger.error(f"Error displaying weather summary: {str(e)}")
        st.warning("Weather information temporarily unavailable")

def display_health_metrics() -> None:
    """Display key health metrics and alerts for the poultry farm."""
    try:
        with st.container():
            st.markdown("### Health Metrics")
            health.display_health_summary()
    except Exception as e:
        logger.error(f"Error displaying health metrics: {str(e)}")
        st.warning("Health metrics temporarily unavailable")

def display_market_trends() -> None:
    """Display current market trends and financial indicators."""
    try:
        with st.container():
            st.markdown("### Market Trends")
            financial.display_market_summary()
    except Exception as e:
        logger.error(f"Error displaying market trends: {str(e)}")
        st.warning("Market trends temporarily unavailable")

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