import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def get_news_data(query: str = "poultry farming") -> dict:
    """Fetch news data from News API with error handling."""
    try:
        api_key = st.secrets["news_api_key"]
        url = "https://newsapi.org/v2/everything"
        
        # Get news from the last 30 days
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'apiKey': api_key,
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except KeyError:
        logger.error("News API key not found in secrets")
        return {"error": "API key not configured"}
    except requests.RequestException as e:
        logger.error(f"News API request failed: {str(e)}")
        return {"error": "News service temporarily unavailable"}

def display_news_card(article: dict) -> None:
    """Display a single news article in a card format."""
    try:
        with st.container():
            st.markdown(f"""
                <div class="modern-card">
                    <h3>{article.get('title', 'No title available')}</h3>
                    <p>{article.get('description', 'No description available')}</p>
                    <p><small>Published: {article.get('publishedAt', 'Date unknown')[:10]}</small></p>
                    <a href="{article.get('url', '#')}" target="_blank">Read more</a>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying news card: {str(e)}")
        st.warning("Unable to display this news article")

def show_news_module():
    """Main news module display."""
    st.markdown("## Poultry Industry News")
    
    try:
        # News categories
        category = st.selectbox(
            "Select News Category",
            ["Industry Updates", "Market News", "Health & Disease", "Technology", "Regulations"]
        )
        
        # Fetch news based on category
        search_query = f"poultry farming {category.lower()}"
        news_data = get_news_data(search_query)
        
        if "error" in news_data:
            st.warning(news_data["error"])
            return
            
        articles = news_data.get("articles", [])
        
        if not articles:
            st.info("No news articles found for this category.")
            return
            
        # Display news articles
        for article in articles[:5]:  # Show top 5 articles
            display_news_card(article)
            
        # Add a "Load More" button
        if len(articles) > 5:
            if st.button("Load More Articles"):
                for article in articles[5:10]:
                    display_news_card(article)
                    
    except Exception as e:
        logger.error(f"Error in news module: {str(e)}")
        st.error("Unable to load news module. Please try again later.")

def format_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("%B %d, %Y")

def show_news():
    st.markdown("<h2>Poultry Industry News & Updates</h2>", unsafe_allow_html=True)
    
    api_key = st.secrets["news_api_key"]
    
    try:
        # Get news about poultry industry
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q=poultry+farming+OR+chicken+industry+OR+egg+production"
            f"&from={start_date.strftime('%Y-%m-%d')}"
            f"&to={end_date.strftime('%Y-%m-%d')}"
            f"&sortBy=publishedAt"
            f"&language=en"
            f"&apiKey={api_key}"
        )
        
        response = requests.get(url)
        news_data = response.json()
        
        if news_data.get('status') == 'ok' and news_data.get('articles'):
            # Filter and sort articles
            articles = news_data['articles']
            
            # Categories for news filtering
            categories = ["All", "Market Updates", "Technology", "Health", "Sustainability"]
            selected_category = st.selectbox("Filter by Category", categories)
            
            # Search functionality
            search_term = st.text_input("Search News", "")
            
            # Filter articles based on category and search term
            filtered_articles = []
            for article in articles:
                if selected_category == "All" or selected_category.lower() in article['title'].lower():
                    if not search_term or search_term.lower() in article['title'].lower():
                        filtered_articles.append(article)
            
            # Display articles in modern cards
            for article in filtered_articles:
                st.markdown("""
                <div class="modern-card" style="margin-bottom: 1.5rem;">
                """, unsafe_allow_html=True)
                
                # Article layout
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    if article.get('urlToImage'):
                        st.image(
                            article['urlToImage'],
                            use_column_width=True,
                            caption="",
                        )
                
                with col2:
                    st.markdown(f"""
                    <h3 style="margin: 0; color: #2c3e50;">{article['title']}</h3>
                    <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
                        {format_date(article['publishedAt'])} | {article['source']['name']}
                    </p>
                    <p style="color: #444; margin: 1rem 0;">
                        {article.get('description', '')}
                    </p>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Read More", key=article['url']):
                        st.markdown(f"[Read the full article]({article['url']})")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
        else:
            st.error("Unable to fetch news articles. Please try again later.")
            
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        
    # Industry Updates Section
    st.markdown("""
    <div class="modern-card">
        <h3>Industry Highlights</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px;">
                <h4 style="color: #2E7D32; margin: 0;">Market Trends</h4>
                <p style="margin: 0.5rem 0 0 0;">Latest updates on poultry market prices and demand patterns</p>
            </div>
            <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px;">
                <h4 style="color: #2E7D32; margin: 0;">Research & Development</h4>
                <p style="margin: 0.5rem 0 0 0;">New technologies and breeding techniques in poultry farming</p>
            </div>
            <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px;">
                <h4 style="color: #2E7D32; margin: 0;">Policy Updates</h4>
                <p style="margin: 0.5rem 0 0 0;">Recent regulations and government policies affecting the industry</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)