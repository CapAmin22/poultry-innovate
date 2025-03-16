import requests
import pandas as pd
from typing import Dict, Any, Optional
import streamlit as st
from urllib.parse import quote

class DataGovClient:
    BASE_URL = "https://api.data.gov.in/resource"

    def __init__(self):
        self.api_key = st.secrets["DATA_GOV_API_KEY"]
        self.resource_id = st.secrets["DATA_GOV_RESOURCE_ID"]
        self.base_url = "https://api.data.gov.in/resource"

    def get_poultry_stats(self, limit: int = 100, offset: int = 0) -> Optional[Dict[str, Any]]:
        """
        Fetch poultry statistics from data.gov.in
        """
        try:
            # Validate API credentials
            if not self.api_key or not self.resource_id:
                st.warning("API credentials not configured properly")
                return self.get_mock_data()

            # Build URL with proper encoding
            url = f"{self.BASE_URL}/{quote(self.resource_id)}"

            # Prepare request parameters
            params = {
                "api-key": self.api_key,
                "format": "json",
                "offset": str(offset),
                "limit": str(limit)
            }

            # Make request with logging
            st.info("Fetching data from data.gov.in...")
            response = requests.get(url, params=params)

            # Log response for debugging
            if response.status_code != 200:
                st.warning(f"API Error: {response.status_code} - {response.text}")
                return self.get_mock_data()

            data = response.json()

            if not data.get('records'):
                st.warning("No records found in API response")
                return self.get_mock_data()

            return data

        except requests.RequestException as e:
            st.warning(f"Network error: {str(e)}. Using sample data instead.")
            return self.get_mock_data()
        except Exception as e:
            st.warning(f"Unexpected error: {str(e)}. Using sample data instead.")
            return self.get_mock_data()

    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the raw API response into a structured format
        """
        try:
            if not raw_data or 'records' not in raw_data:
                return self.get_mock_data()

            records = raw_data['records']

            # Add debug information
            st.info(f"Processing {len(records)} records from API")

            # Create production time series
            production_data = []
            prices_data = []
            total_production = 0
            total_price = 0
            price_count = 0

            for record in records:
                # Process each record
                # Note: Update these field names based on actual API response structure
                if 'production_value' in record:
                    production_data.append({
                        'date': record.get('date', ''),
                        'value': float(record['production_value'])
                    })
                    total_production += float(record['production_value'])

                if 'price' in record:
                    price = float(record['price'])
                    prices_data.append({
                        'region': record.get('region', 'Unknown'),
                        'price': price
                    })
                    total_price += price
                    price_count += 1

            # Calculate metrics
            avg_price = total_price / price_count if price_count > 0 else 0

            processed_data = {
                'production': pd.DataFrame(production_data),
                'prices': pd.DataFrame(prices_data),
                'metrics': {
                    'total_production': round(total_production, 2),
                    'avg_price': round(avg_price, 2),
                    'growth_rate': 5.2  # This will be calculated from historical data
                }
            }

            return processed_data

        except Exception as e:
            st.warning(f"Error processing data: {str(e)}. Using sample data instead.")
            return self.get_mock_data()

    def get_mock_data(self) -> Dict[str, Any]:
        """
        Fallback mock data when API is not configured or fails
        """
        from .mock_statistics import get_mock_data
        return get_mock_data()