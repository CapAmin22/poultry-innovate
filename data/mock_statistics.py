import pandas as pd
import numpy as np

def get_mock_data():
    # Production data
    months = pd.date_range(start='2023-01-01', periods=12, freq='M')
    production_data = pd.DataFrame({
        'month': months,
        'value': np.random.normal(100000, 5000, 12)
    })
    
    # Price data
    price_data = pd.DataFrame({
        'region': ['North', 'South', 'East', 'West'],
        'price': np.random.uniform(90, 120, 4)
    })
    
    # Feed costs
    feed_data = pd.DataFrame({
        'type': ['Corn', 'Soybean', 'Minerals', 'Others'],
        'cost': [45, 30, 15, 10]
    })
    
    # Key metrics
    metrics = {
        'total_production': round(production_data['value'].sum() / 1000, 2),
        'avg_price': round(price_data['price'].mean(), 2),
        'growth_rate': round(np.random.uniform(5, 15), 2)
    }
    
    return {
        'production': production_data,
        'prices': price_data,
        'feed_costs': feed_data,
        'metrics': metrics
    }
