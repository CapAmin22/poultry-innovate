import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import pytz

logger = logging.getLogger(__name__)

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_icon(icon_code):
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def get_weather_data(city: str = None) -> dict:
    """
    Fetch weather data from OpenWeather API with proper error handling.
    """
    try:
        if not city:
            city = st.secrets.weather.get("default_city", "Manila")
        
        api_key = st.secrets.openweather_api_key
        base_url = f"{st.secrets.api_urls.weather}/weather"
        
        params = {
            "q": city,
            "appid": api_key,
            "units": st.secrets.weather.get("units", "metric")
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in weather data fetch: {str(e)}")
        return None

def display_weather_widget():
    """Display weather information in a modern card format."""
    try:
        # Get user's location or use default
        city = st.session_state.get('user_location', st.secrets.weather.get("default_city", "Manila"))
        
        # Location input
        new_city = st.text_input("Enter location:", value=city, key="weather_location")
        if new_city != city:
            st.session_state.user_location = new_city
            st.rerun()
        
        weather_data = get_weather_data(new_city)
        
        if weather_data:
            # Convert timestamp to local time
            timestamp = datetime.fromtimestamp(weather_data["dt"])
            ph_tz = pytz.timezone("Asia/Manila")
            local_time = timestamp.astimezone(ph_tz)
            
            # Display weather information
            st.markdown(f"""
            <div class="modern-card" style="padding: 1.5rem;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <h4 style="margin: 0; color: #ffffff;">{weather_data["name"]}</h4>
                        <p style="margin: 0; color: rgba(255,255,255,0.7);">
                            {local_time.strftime("%I:%M %p, %B %d")}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <h2 style="margin: 0; color: #ffffff;">
                            {weather_data["main"]["temp"]}°C
                        </h2>
                        <p style="margin: 0; color: rgba(255,255,255,0.7);">
                            {weather_data["weather"][0]["description"].title()}
                        </p>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem;">
                    <div>
                        <p style="margin: 0; color: rgba(255,255,255,0.7);">Humidity</p>
                        <p style="margin: 0; color: #ffffff; font-size: 1.1rem;">
                            {weather_data["main"]["humidity"]}%
                        </p>
                    </div>
                    <div>
                        <p style="margin: 0; color: rgba(255,255,255,0.7);">Wind</p>
                        <p style="margin: 0; color: #ffffff; font-size: 1.1rem;">
                            {weather_data["wind"]["speed"]} m/s
                        </p>
                    </div>
                    <div>
                        <p style="margin: 0; color: rgba(255,255,255,0.7);">Pressure</p>
                        <p style="margin: 0; color: #ffffff; font-size: 1.1rem;">
                            {weather_data["main"]["pressure"]} hPa
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Unable to fetch weather data. Please check your location and try again.")
            
    except Exception as e:
        logger.error(f"Error displaying weather widget: {str(e)}")
        st.error("Error displaying weather information. Please try again later.")

def show_weather_module():
    """Main weather module display."""
    st.markdown("## Weather Information")
    
    try:
        # Main weather display
        display_weather_widget()
        
        # Additional weather information
        if st.session_state.get('user_location'):
            weather_data = get_weather_data(st.session_state.user_location)
            if weather_data:
                st.markdown("### Detailed Weather Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="modern-card" style="padding: 1.5rem;">
                        <h4 style="margin: 0 0 1rem 0; color: #ffffff;">Temperature Range</h4>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.7);">Min</p>
                                <p style="margin: 0; color: #ffffff; font-size: 1.2rem;">
                                    {:.1f}°C
                                </p>
                            </div>
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.7);">Max</p>
                                <p style="margin: 0; color: #ffffff; font-size: 1.2rem;">
                                    {:.1f}°C
                                </p>
                            </div>
                        </div>
                    </div>
                    """.format(
                        weather_data["main"]["temp_min"],
                        weather_data["main"]["temp_max"]
                    ), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="modern-card" style="padding: 1.5rem;">
                        <h4 style="margin: 0 0 1rem 0; color: #ffffff;">Visibility & Clouds</h4>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.7);">Visibility</p>
                                <p style="margin: 0; color: #ffffff; font-size: 1.2rem;">
                                    {} km
                                </p>
                            </div>
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.7);">Cloud Cover</p>
                                <p style="margin: 0; color: #ffffff; font-size: 1.2rem;">
                                    {}%
                                </p>
                            </div>
                        </div>
                    </div>
                    """.format(
                        weather_data["visibility"] / 1000,
                        weather_data["clouds"]["all"]
                    ), unsafe_allow_html=True)
                
                # Weather Impact Analysis
                st.markdown("### Weather Impact Analysis")
                
                impact_analysis = analyze_weather_impact(weather_data)
                
                for category, details in impact_analysis.items():
                    st.markdown(f"""
                    <div class="modern-card" style="padding: 1.5rem; margin-bottom: 1rem;">
                        <h4 style="margin: 0 0 0.5rem 0; color: #ffffff;">{category}</h4>
                        <p style="margin: 0; color: rgba(255,255,255,0.9);">{details["description"]}</p>
                        <div style="margin-top: 0.5rem;">
                            <span style="color: {details['color']};">Impact Level: {details['impact']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    except Exception as e:
        logger.error(f"Error in weather module: {str(e)}")
        st.error("Error loading weather module. Please try again later.")

def analyze_weather_impact(weather_data: dict) -> dict:
    """Analyze weather data and provide impact assessment for farming operations."""
    try:
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        analysis = {
            "Poultry Health": {
                "description": "",
                "impact": "",
                "color": ""
            },
            "Feed Management": {
                "description": "",
                "impact": "",
                "color": ""
            },
            "Facility Operations": {
                "description": "",
                "impact": "",
                "color": ""
            }
        }
        
        # Analyze temperature impact
        if 18 <= temp <= 26:
            analysis["Poultry Health"].update({
                "description": "Optimal temperature range for poultry. Good conditions for growth and production.",
                "impact": "Low",
                "color": "#00ff87"
            })
        elif temp < 18:
            analysis["Poultry Health"].update({
                "description": "Temperature below optimal range. Consider additional heating.",
                "impact": "Moderate",
                "color": "#ffaa00"
            })
        else:
            analysis["Poultry Health"].update({
                "description": "High temperature alert. Implement cooling measures.",
                "impact": "High",
                "color": "#ff4444"
            })
        
        # Analyze humidity impact
        if 40 <= humidity <= 60:
            analysis["Facility Operations"].update({
                "description": "Optimal humidity range. Maintain current ventilation settings.",
                "impact": "Low",
                "color": "#00ff87"
            })
        elif humidity < 40:
            analysis["Facility Operations"].update({
                "description": "Low humidity. Consider using humidifiers or misting systems.",
                "impact": "Moderate",
                "color": "#ffaa00"
            })
        else:
            analysis["Facility Operations"].update({
                "description": "High humidity. Increase ventilation to prevent moisture-related issues.",
                "impact": "High",
                "color": "#ff4444"
            })
        
        # Analyze wind impact on feed management
        if wind_speed < 5:
            analysis["Feed Management"].update({
                "description": "Calm conditions. Optimal for outdoor feeding operations.",
                "impact": "Low",
                "color": "#00ff87"
            })
        elif 5 <= wind_speed <= 10:
            analysis["Feed Management"].update({
                "description": "Moderate wind. Monitor outdoor feeding areas.",
                "impact": "Moderate",
                "color": "#ffaa00"
            })
        else:
            analysis["Feed Management"].update({
                "description": "Strong winds. Consider moving feeding operations indoors.",
                "impact": "High",
                "color": "#ff4444"
            })
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in weather impact analysis: {str(e)}")
        return {}

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