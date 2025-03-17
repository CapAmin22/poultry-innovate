import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def get_news_data(query: str = "poultry farming", days: int = 7) -> list:
    """
    Fetch news data from News API with proper error handling.
    """
    try:
        api_key = st.secrets.news_api_key
        base_url = f"{st.secrets.api_urls.news}/everything"
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        params = {
            "q": query,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "sortBy": "relevancy",
            "language": "en",
            "apiKey": api_key
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("articles", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news data: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in news data fetch: {str(e)}")
        return []

def display_news_card(article: dict):
    """Display a single news article in a modern card format."""
    try:
        # Format the publication date
        pub_date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = pub_date.strftime("%B %d, %Y")
        
        st.markdown(f"""
        <div class="modern-card" style="padding: 1.5rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #ffffff;">
                        {article["title"]}
                    </h4>
                    <p style="margin: 0 0 1rem 0; color: rgba(255,255,255,0.7);">
                        {formatted_date} • {article["source"]["name"]}
                    </p>
                    <p style="margin: 0; color: rgba(255,255,255,0.9);">
                        {article["description"]}
                    </p>
                </div>
                {f'<img src="{article["urlToImage"]}" style="width: 150px; height: 100px; object-fit: cover; margin-left: 1rem; border-radius: 4px;" alt="News Image"/>' if article.get("urlToImage") else ''}
            </div>
            <div style="margin-top: 1rem;">
                <a href="{article["url"]}" target="_blank" style="color: #00ff87; text-decoration: none;">
                    Read more →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying news card: {str(e)}")

def show_news_module():
    """Main news module display."""
    st.markdown("## Industry News & Updates")
    
    try:
        # News filters
        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input(
                "Search news:",
                value="poultry farming",
                key="news_search"
            )
        with col2:
            days_filter = st.selectbox(
                "Time period:",
                options=[7, 14, 30],
                format_func=lambda x: f"Last {x} days",
                key="news_days"
            )
        
        # Fetch news articles
        articles = get_news_data(search_query, days_filter)
        
        if articles:
            # Display articles in modern cards
            for article in articles:
                display_news_card(article)
            
            # Add load more button if needed
            if len(articles) >= 10:
                st.button("Load More", key="load_more_news")
        else:
            st.info("No news articles found. Try adjusting your search criteria.")
        
    except Exception as e:
        logger.error(f"Error in news module: {str(e)}")
        st.error("Error loading news module. Please try again later.")

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