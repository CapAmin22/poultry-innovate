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
    /* Modern Card Styling */
    .stApp {
        background-color: #f8f9fa;
    }

    .css-1d391kg {
        padding-top: 1rem;
    }

    /* Bottom Navigation */
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 999;
        padding: 0.5rem;
    }

    .stButton>button {
        background: none;
        border: none;
        color: #555;
        font-size: 0.8rem;
        padding: 0.5rem;
        border-radius: 50%;
        aspect-ratio: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        color: #ff4b4b;
        background: none;
    }

    .stButton>button[data-active="true"] {
        color: #ff4b4b;
    }

    /* Card Styling */
    .modern-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
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