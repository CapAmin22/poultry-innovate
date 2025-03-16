import streamlit as st
from modules import weather, news, statistics, education, financial, stakeholders

st.set_page_config(
    page_title="Indian Poultry Platform",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern mobile-first CSS
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }

    .css-1d391kg {
        padding-top: 1.5rem;
    }

    /* Typography Improvements */
    h1, h2, h3 {
        color: #1a1a1a;
        font-family: 'Segoe UI', system-ui, sans-serif;
        letter-spacing: -0.5px;
    }

    p {
        color: #444;
        line-height: 1.6;
    }

    /* Bottom Navigation */
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
        z-index: 999;
        padding: 0.8rem;
        border-top: 1px solid rgba(0,0,0,0.05);
    }

    .stButton>button {
        background: none;
        border: none;
        color: #666;
        font-size: 0.85rem;
        padding: 0.6rem;
        border-radius: 12px;
        aspect-ratio: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        font-weight: 500;
    }

    .stButton>button:hover {
        color: #ff4b4b;
        background: rgba(255,75,75,0.1);
        transform: translateY(-2px);
    }

    .stButton>button[data-active="true"] {
        color: #ff4b4b;
        background: rgba(255,75,75,0.1);
    }

    /* Card Styling */
    .modern-card {
        background: white;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin-bottom: 1.2rem;
        border: 1px solid rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox select {
        border-radius: 8px;
        border: 1px solid rgba(0,0,0,0.1);
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #ff4b4b;
        box-shadow: 0 0 0 2px rgba(255,75,75,0.2);
    }

    /* DataFrames and Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.1);
    }

    .dataframe th {
        background: #f8f9fa;
        padding: 0.75rem 1rem;
    }

    .dataframe td {
        padding: 0.75rem 1rem;
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-bottom: 6rem;}
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Dashboard"

    # Content area with padding for bottom navigation
    st.markdown('<div style="padding-bottom: 70px;">', unsafe_allow_html=True)

    # Main content based on active tab
    if st.session_state.active_tab == "Dashboard":
        statistics.show_dashboard()
    elif st.session_state.active_tab == "Education":
        education.show_content()
    elif st.session_state.active_tab == "Weather":
        with st.spinner("Fetching weather data..."):
            weather.show_forecast()
    elif st.session_state.active_tab == "Finance":
        financial.show_assistance()
    elif st.session_state.active_tab == "Network":
        stakeholders.show_directory()
    elif st.session_state.active_tab == "News":
        with st.spinner("Loading latest news..."):
            news.show_news()

    st.markdown('</div>', unsafe_allow_html=True)

    # Modern Bottom Navigation
    st.markdown("""
    <div class="nav-container">
        <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px;">
    """, unsafe_allow_html=True)

    # Navigation buttons
    nav_items = [
        ("📊", "Dashboard", "Stats"),
        ("📚", "Education", "Learn"),
        ("🌤️", "Weather", "Weather"),
        ("💰", "Finance", "Finance"),
        ("👥", "Network", "Network"),
        ("📰", "News", "News")
    ]

    for icon, tab, tooltip in nav_items:
        is_active = st.session_state.active_tab == tab
        col_html = f"""
        <div style="text-align: center;">
            <button 
                onclick="parent.document.querySelector('button[data-testid=\\"stButton-{tab.lower()}\\"]').click();"
                style="background: none; border: none; color: {'#ff4b4b' if is_active else '#555'}; 
                       padding: 8px; width: 100%; cursor: pointer;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-size: 0.7rem;">{tooltip}</div>
            </button>
        </div>
        """
        st.markdown(col_html, unsafe_allow_html=True)

        # Hidden button for state management
        if st.button(tab, key=tab.lower(), help=tooltip):
            st.session_state.active_tab = tab
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()