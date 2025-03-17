import streamlit as st
import requests
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

class APIConfig:
    def __init__(self):
        try:
            # Get API keys from Streamlit secrets
            self.weather_api_key = st.secrets["openweather_api_key"]
            self.news_api_key = st.secrets["news_api_key"]
            
            # API Base URLs from secrets
            self.weather_base_url = st.secrets.get("api_urls", {}).get("weather", "https://api.openweathermap.org/data/2.5")
            self.news_base_url = st.secrets.get("api_urls", {}).get("news", "https://newsapi.org/v2")
            self.market_base_url = st.secrets.get("api_urls", {}).get("market", None)
            
            logger.info("API configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading API configuration: {e}")
            raise RuntimeError("Failed to load API configuration")

    def get_headers(self, api_type):
        """Get headers for different API types"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if api_type == 'weather':
            headers['Authorization'] = f'Bearer {self.weather_api_key}'
        elif api_type == 'news':
            headers['X-Api-Key'] = self.news_api_key
            
        return headers

def api_error_handler(func):
    """Decorator to handle API errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                retry_count += 1
                if retry_count == max_retries:
                    logger.error(f"API request failed after {max_retries} retries: {str(e)}")
                    return {
                        'error': True,
                        'message': str(e),
                        'status_code': getattr(e.response, 'status_code', 500)
                    }
                logger.warning(f"API request failed, attempt {retry_count} of {max_retries}")
                time.sleep(1)  # Wait before retrying
                
    return wrapper

class APIClient:
    def __init__(self):
        self.config = APIConfig()
    
    @api_error_handler
    def get_weather(self, city, country='IN'):
        """Get weather data"""
        params = {
            'q': f'{city},{country}',
            'appid': self.config.weather_api_key,
            'units': 'metric'
        }
        response = requests.get(f'{self.config.weather_base_url}/forecast', params=params)
        response.raise_for_status()
        return response.json()
    
    @api_error_handler
    def get_news(self, query='poultry farming', days=30):
        """Get news articles"""
        params = {
            'q': query,
            'apiKey': self.config.news_api_key,
            'language': 'en',
            'from': (time.time() - days * 86400)  # Convert days to seconds
        }
        response = requests.get(f'{self.config.news_base_url}/everything', params=params)
        response.raise_for_status()
        return response.json()
    
    @api_error_handler
    def get_market_prices(self, commodity='poultry'):
        """Get market prices using dummy data"""
        return {
            'data': st.secrets.get("dummy_market_data", {}).get("commodities", []),
            'timestamp': time.time()
        }

# Create a singleton instance
api_client = APIClient() 