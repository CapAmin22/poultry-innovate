import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import load_lottie_url

class TestPoultryInnovate(unittest.TestCase):
    """Test cases for the PoultryInnovate application."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_url = "https://assets5.lottiefiles.com/packages/lf20_GofK09iPAE.json"
        self.mock_lottie_data = {"v": "5.5.7", "fr": 60, "ip": 0, "op": 180, "w": 512, "h": 512}

    @patch('requests.get')
    def test_load_lottie_url_success(self, mock_get):
        """Test successful loading of Lottie animation."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_lottie_data
        mock_get.return_value = mock_response

        # Test the function
        result = load_lottie_url(self.test_url)
        
        # Verify the results
        self.assertEqual(result, self.mock_lottie_data)
        mock_get.assert_called_once_with(self.test_url)

    @patch('requests.get')
    def test_load_lottie_url_failure(self, mock_get):
        """Test failed loading of Lottie animation."""
        # Configure the mock to raise an exception
        mock_get.side_effect = Exception("Network error")

        # Test the function
        result = load_lottie_url(self.test_url)
        
        # Verify the results
        self.assertIsNone(result)
        mock_get.assert_called_once_with(self.test_url)

    @patch('requests.get')
    def test_load_lottie_url_bad_status(self, mock_get):
        """Test loading Lottie animation with bad HTTP status."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")
        mock_get.return_value = mock_response

        # Test the function
        result = load_lottie_url(self.test_url)
        
        # Verify the results
        self.assertIsNone(result)
        mock_get.assert_called_once_with(self.test_url)

if __name__ == '__main__':
    unittest.main() 