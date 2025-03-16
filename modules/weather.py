import streamlit as st
import requests
from datetime import datetime
import pandas as pd

def get_weather_data(city="Delhi"):
    api_key = st.secrets.get("WEATHER_API_KEY", "")
    if not api_key:
        st.error("Weather API key not configured")
        return None
    
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def show_forecast():
    st.header("Weather Forecast and Impact Analysis")
    
    city = st.selectbox(
        "Select City",
        ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"]
    )
    
    weather_data = get_weather_data(city)
    
    if weather_data:
        st.subheader(f"5-Day Weather Forecast for {city}")
        
        forecast_data = []
        for item in weather_data['list'][:8]:
            date = datetime.fromtimestamp(item['dt'])
            forecast_data.append({
                'Date': date.strftime('%Y-%m-%d %H:%M'),
                'Temperature': item['main']['temp'],
                'Humidity': item['main']['humidity'],
                'Description': item['weather'][0]['description']
            })
        
        df = pd.DataFrame(forecast_data)
        st.dataframe(df)
        
        st.subheader("Impact Analysis")
        if df['Temperature'].mean() > 35:
            st.warning("High temperatures may affect poultry health and productivity")
        elif df['Temperature'].mean() < 15:
            st.warning("Low temperatures may require additional heating in poultry houses")
        
        if df['Humidity'].mean() > 80:
            st.warning("High humidity levels may increase disease risks")
