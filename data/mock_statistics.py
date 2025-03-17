import pandas as pd
import numpy as np

def get_mock_data():
    # Generate dates for the last 12 months
    months = pd.date_range(start='2023-01-01', periods=12, freq='M')
    
    # Monthly egg production (with seasonal variation)
    base_production = 8500
    seasonal_factor = np.sin(np.linspace(0, 2*np.pi, 12)) * 1000
    noise = np.random.normal(0, 200, 12)
    monthly_production = pd.Series(
        base_production + seasonal_factor + noise,
        index=months
    ).round()
    
    # Feed consumption (correlated with production)
    base_feed = 2500
    feed_variation = seasonal_factor * 0.3
    feed_noise = np.random.normal(0, 100, 12)
    feed_consumption = pd.Series(
        base_feed + feed_variation + feed_noise,
        index=months
    ).round()
    
    # Mortality rate (low with occasional spikes)
    base_mortality = 0.8
    mortality_spikes = np.random.choice([0, 0.5], size=12, p=[0.8, 0.2])
    mortality_noise = np.random.normal(0, 0.1, 12)
    mortality_rate = pd.Series(
        base_mortality + mortality_spikes + mortality_noise,
        index=months
    ).clip(0, 5)  # Cap between 0% and 5%
    
    # Revenue data (correlated with production)
    egg_price = 0.15  # price per egg
    revenue_noise = np.random.normal(0, 500, 12)
    revenue_data = pd.Series(
        monthly_production * egg_price + revenue_noise,
        index=months
    ).round()
    
    return monthly_production, feed_consumption, mortality_rate, revenue_data
