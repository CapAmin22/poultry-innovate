import streamlit as st
import requests
from datetime import datetime, timedelta

def get_news():
    api_key = st.secrets.get("NEWS_API_KEY", "")
    if not api_key:
        st.error("News API key not configured")
        return None
    
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
        st.error(f"Error fetching news: {str(e)}")
        return None

def show_news():
    st.header("Industry News and Updates")
    
    news_data = get_news()
    
    if news_data and news_data.get('articles'):
        for article in news_data['articles'][:10]:
            with st.expander(article['title']):
                st.write(article['description'])
                st.write(f"Published: {article['publishedAt'][:10]}")
                st.link_button("Read More", article['url'])
