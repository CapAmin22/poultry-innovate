import streamlit as st
import requests
from datetime import datetime, timedelta

def get_news():
    api_key = st.secrets.get("NEWS_API_KEY", "")
    if not api_key:
        return get_mock_news()

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "poultry India",
        "apiKey": api_key,
        "language": "en",
        "from": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.warning("Unable to fetch live news, showing sample updates.")
        return get_mock_news()

def get_mock_news():
    """Provide sample news data for demonstration"""
    return {
        'articles': [
            {
                'title': 'Indian Poultry Market Shows Strong Growth',
                'description': 'The Indian poultry industry continues to show robust growth with increasing demand for quality protein sources.',
                'publishedAt': datetime.now().strftime('%Y-%m-%d'),
                'url': '#'
            },
            {
                'title': 'New Technologies in Poultry Farming',
                'description': 'Smart farming technologies are revolutionizing the Indian poultry sector.',
                'publishedAt': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'url': '#'
            },
            {
                'title': 'Sustainable Practices in Poultry Industry',
                'description': 'Indian farmers are adopting eco-friendly practices in poultry farming.',
                'publishedAt': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'url': '#'
            }
        ]
    }

def show_news():
    st.header("Industry News and Updates")

    news_data = get_news()

    if news_data and news_data.get('articles'):
        for article in news_data['articles'][:10]:
            with st.expander(article['title']):
                st.write(article['description'])
                st.write(f"Published: {article['publishedAt'][:10]}")
                if article['url'] != '#':
                    st.link_button("Read More", article['url'])