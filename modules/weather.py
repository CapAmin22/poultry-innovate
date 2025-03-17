import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_icon(icon_code):
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def get_weather_data(lat: float = 0, lon: float = 0) -> dict:
    """Fetch weather data from OpenWeather API with error handling."""
    try:
        api_key = st.secrets["openweather_api_key"]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except KeyError:
        logger.error("OpenWeather API key not found in secrets")
        return {"error": "API key not configured"}
    except requests.RequestException as e:
        logger.error(f"Weather API request failed: {str(e)}")
        return {"error": "Weather service temporarily unavailable"}

def display_weather_widget():
    """Display weather information with error handling."""
    try:
        # Default coordinates (can be updated based on user location)
        weather_data = get_weather_data(14.5995, 120.9842)  # Manila coordinates
        
        if "error" in weather_data:
            st.warning(weather_data["error"])
            return
            
        temp = weather_data.get("main", {}).get("temp", "N/A")
        humidity = weather_data.get("main", {}).get("humidity", "N/A")
        description = weather_data.get("weather", [{}])[0].get("description", "N/A").capitalize()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{temp}°C")
        with col2:
            st.metric("Humidity", f"{humidity}%")
        with col3:
            st.metric("Conditions", description)
            
    except Exception as e:
        logger.error(f"Error displaying weather widget: {str(e)}")
        st.warning("Weather information temporarily unavailable")

def show_weather_module():
    """Main weather module display."""
    st.markdown("## Weather Monitoring")
    
    try:
        # Location selector (can be enhanced with geocoding)
        st.selectbox("Select Location", ["Manila", "Cebu", "Davao"], key="weather_location")
        
        # Current conditions
        st.markdown("### Current Conditions")
        display_weather_widget()
        
        # Forecast section
        st.markdown("### 5-Day Forecast")
        st.info("Forecast feature coming soon!")
        
    except Exception as e:
        logger.error(f"Error in weather module: {str(e)}")
        st.error("Unable to load weather module. Please try again later.")

def show_forecast(location=None):
    if not location:
        st.warning("Please set your location to view weather forecasts.")
        return

    api_key = st.secrets["openweather_api_key"]
    
    try:
        # Get coordinates for the location
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data:
            st.error("Location not found. Please try another location.")
            return
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # Get current weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        current_response = requests.get(current_url)
        current_data = current_response.json()
        
        # Get 5-day forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        
        # Display current weather in a modern card
        st.markdown("""
        <div class="modern-card">
            <h3>Current Weather</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            icon_code = current_data['weather'][0]['icon']
            st.image(get_weather_icon(icon_code), width=100)
            
        with col2:
            temp_c = kelvin_to_celsius(current_data['main']['temp'])
            feels_like_c = kelvin_to_celsius(current_data['main']['feels_like'])
            
            st.markdown(f"""
            <div style="padding: 1rem;">
                <h2 style="color: #4CAF50; margin: 0;">{temp_c:.1f}°C</h2>
                <p style="margin: 0.5rem 0;">Feels like: {feels_like_c:.1f}°C</p>
                <p style="margin: 0.5rem 0; text-transform: capitalize;">{current_data['weather'][0]['description']}</p>
                <p style="margin: 0.5rem 0;">Humidity: {current_data['main']['humidity']}%</p>
                <p style="margin: 0.5rem 0;">Wind: {current_data['wind']['speed']} m/s</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display 5-day forecast
        st.markdown("""
        <div class="modern-card">
            <h3>5-Day Forecast</h3>
        """, unsafe_allow_html=True)
        
        # Prepare data for the chart
        dates = []
        temps = []
        humidity = []
        icons = []
        
        for item in forecast_data['list'][::8]:  # Get one reading per day
            date = datetime.fromtimestamp(item['dt'])
            dates.append(date.strftime('%A'))  # Day name
            temps.append(kelvin_to_celsius(item['main']['temp']))
            humidity.append(item['main']['humidity'])
            icons.append(item['weather'][0]['icon'])
        
        # Create temperature chart
        fig = go.Figure()
        
        # Add temperature line
        fig.add_trace(go.Scatter(
            x=dates,
            y=temps,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=10, symbol='diamond')
        ))
        
        # Add humidity bars
        fig.add_trace(go.Bar(
            x=dates,
            y=humidity,
            name='Humidity %',
            marker_color='rgba(76, 175, 80, 0.2)',
            yaxis='y2'
        ))
        
        # Update layout
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, l=20, r=20, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#f0f0f0',
                title='Temperature (°C)'
            ),
            yaxis2=dict(
                title='Humidity (%)',
                overlaying='y',
                side='right',
                showgrid=False,
                range=[0, 100]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display daily forecast cards
        cols = st.columns(5)
        for i, (date, temp, hum, icon) in enumerate(zip(dates, temps, humidity, icons)):
            with cols[i]:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <p style="margin: 0; font-weight: bold;">{date}</p>
                    <img src="{get_weather_icon(icon)}" style="width: 50px; height: 50px;">
                    <p style="margin: 0; color: #4CAF50;">{temp:.1f}°C</p>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">{hum}% humidity</p>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Weather advisory
        st.markdown("""
        <div class="modern-card">
            <h3>Weather Advisory for Poultry Farming</h3>
            <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        # Generate weather advice based on conditions
        temp = kelvin_to_celsius(current_data['main']['temp'])
        humidity = current_data['main']['humidity']
        
        if temp > 32:
            st.warning("⚠️ High Temperature Alert: Ensure proper ventilation and cooling systems are active.")
        elif temp < 10:
            st.warning("⚠️ Low Temperature Alert: Maintain optimal temperature in poultry houses.")
            
        if humidity > 80:
            st.warning("⚠️ High Humidity Alert: Monitor ventilation to prevent moisture-related issues.")
        elif humidity < 40:
            st.warning("⚠️ Low Humidity Alert: Consider using humidifiers or water spraying systems.")
            
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")