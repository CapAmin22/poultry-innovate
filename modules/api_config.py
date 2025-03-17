import streamlit as st
import requests
from functools import wraps
import time
import logging
import json

logger = logging.getLogger(__name__)

class APIConfig:
    def __init__(self):
        """Initialize API configuration with fallback values."""
        try:
            # API Keys with fallback to dummy values for development
            self.weather_api_key = st.secrets.get("openweather_api_key", "dummy_key")
            self.news_api_key = st.secrets.get("news_api_key", "dummy_key")
            
            # API Base URLs with fallbacks
            self.weather_base_url = st.secrets.get("api_urls", {}).get("weather", "https://api.openweathermap.org/data/2.5")
            self.news_base_url = st.secrets.get("api_urls", {}).get("news", "https://newsapi.org/v2")
            
            # Load dummy market data configuration
            self.dummy_market_data = st.secrets.get("dummy_market_data", {
                "use_dummy_data": True,
                "commodities": {
                    "feed_price": 45.50,
                    "broiler_price": 120.75,
                    "egg_price": 6.25
                }
            })
            
            logger.info("API configuration loaded successfully")
        except Exception as e:
            logger.warning(f"Using fallback configuration: {e}")
            # Set default values instead of raising an error
            self.weather_api_key = "dummy_key"
            self.news_api_key = "dummy_key"
            self.weather_base_url = "https://api.openweathermap.org/data/2.5"
            self.news_base_url = "https://newsapi.org/v2"
            self.dummy_market_data = {
                "use_dummy_data": True,
                "commodities": {
                    "feed_price": 45.50,
                    "broiler_price": 120.75,
                    "egg_price": 6.25
                }
            }

    def get_headers(self, api_type):
        """Get headers for different API types with fallback to empty headers."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            if api_type == 'weather' and self.weather_api_key != "dummy_key":
                headers['Authorization'] = f'Bearer {self.weather_api_key}'
            elif api_type == 'news' and self.news_api_key != "dummy_key":
                headers['X-Api-Key'] = self.news_api_key
        except Exception as e:
            logger.warning(f"Error setting API headers: {e}")
            
        return headers

def api_error_handler(func):
    """Decorator to handle API errors and provide fallback responses."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                retry_count += 1
                logger.warning(f"API request failed (attempt {retry_count}/{max_retries}): {e}")
                if retry_count == max_retries:
                    # Return dummy data on failure
                    return get_dummy_response(func.__name__)
                time.sleep(1)
    return wrapper

def get_dummy_response(endpoint_name):
    """Provide dummy responses for different endpoints."""
    dummy_data = {
        'get_weather': {
            'main': {'temp': 25, 'humidity': 60},
            'weather': [{'description': 'sunny', 'icon': '01d'}],
            'wind': {'speed': 5},
            'dt': time.time()
        },
        'get_news': {
            'articles': [
                {
                    'title': 'Sample Poultry News',
                    'description': 'This is a sample news article about poultry farming.',
                    'url': '#',
                    'publishedAt': '2024-03-17T12:00:00Z',
                    'source': {'name': 'Sample News'}
                }
            ]
        },
        'get_market_prices': {
            'data': st.secrets.get("dummy_market_data", {}).get("commodities", {
                'feed_price': 45.50,
                'broiler_price': 120.75,
                'egg_price': 6.25
            }),
            'timestamp': time.time()
        }
    }
    return dummy_data.get(endpoint_name, {'error': 'No dummy data available'})

class APIClient:
    def __init__(self):
        """Initialize API client with configuration."""
        try:
            self.config = APIConfig()
        except Exception as e:
            logger.error(f"Error initializing API client: {e}")
            self.config = None
    
    @api_error_handler
    def get_weather(self, city, country='IN'):
        """Get weather data with fallback to dummy data."""
        if self.config and self.config.weather_api_key != "dummy_key":
            params = {
                'q': f'{city},{country}',
                'appid': self.config.weather_api_key,
                'units': 'metric'
            }
            response = requests.get(f'{self.config.weather_base_url}/forecast', params=params)
            response.raise_for_status()
            return response.json()
        return get_dummy_response('get_weather')
    
    @api_error_handler
    def get_news(self, query='poultry farming', days=7):
        """Get news articles with fallback to dummy data."""
        if self.config and self.config.news_api_key != "dummy_key":
            params = {
                'q': query,
                'apiKey': self.config.news_api_key,
                'language': 'en',
                'from': time.strftime('%Y-%m-%d', time.localtime(time.time() - days * 86400))
            }
            response = requests.get(f'{self.config.news_base_url}/everything', params=params)
            response.raise_for_status()
            return response.json()
        return get_dummy_response('get_news')
    
    def get_market_prices(self, commodity='poultry'):
        """Get market prices using dummy data."""
        return get_dummy_response('get_market_prices')

# Create a singleton instance with error handling
try:
    api_client = APIClient()
    logger.info("API client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize API client: {e}")
    api_client = None 