import requests
import pandas as pd
from typing import Dict, Any, Optional
import streamlit as st

class DataGovClient:
    BASE_URL = "https://api.data.gov.in/resource"

    def __init__(self):
        self.api_key = st.secrets.get("DATA_GOV_API_KEY", "")
        self.resource_id = st.secrets.get("DATA_GOV_RESOURCE_ID", "")

    def get_poultry_stats(self, limit: int = 100, offset: int = 0) -> Optional[Dict[str, Any]]:
        """
        Fetch poultry statistics from data.gov.in
        """
        if not self.api_key or not self.resource_id:
            return self.get_mock_data()  # Return mock data if keys are not available

        try:
            url = f"{self.BASE_URL}/{self.resource_id}"
            params = {
                "api-key": self.api_key,
                "format": "json",
                "offset": offset,
                "limit": limit
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            st.warning(f"Unable to fetch live data, showing sample statistics instead.")
            return self.get_mock_data()

    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Process the raw API response into pandas DataFrames
        """
        # For now, return mock data since we don't have the actual API structure
        return self.get_mock_data()

    def get_mock_data(self) -> Dict[str, pd.DataFrame]:
        """
        Fallback mock data when API is not configured or fails
        """
        from .mock_statistics import get_mock_data
        return get_mock_data()