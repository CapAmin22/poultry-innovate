import streamlit as st
from modules import weather, news, statistics, education, financial, stakeholders

st.set_page_config(
    page_title="Indian Poultry Platform",
    page_icon="🐔",
    layout="wide"
)

# Custom CSS for Instagram-like UI
st.markdown("""
<style>
    .nav-button {
        background-color: white;
        color: black;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .nav-button:hover {
        background-color: #f0f0f0;
    }
    .nav-button.active {
        color: #ff4b4b;
        border-top: 2px solid #ff4b4b;
    }
    .stButton>button {
        width: 100%;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state for active tab
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Dashboard"

    # Main content area
    if st.session_state.active_tab == "Dashboard":
        statistics.show_dashboard()
    elif st.session_state.active_tab == "Education":
        education.show_content()
    elif st.session_state.active_tab == "Weather":
        weather.show_forecast()
    elif st.session_state.active_tab == "Finance":
        financial.show_assistance()
    elif st.session_state.active_tab == "Network":
        stakeholders.show_directory()
    elif st.session_state.active_tab == "News":
        news.show_news()

    # Bottom Navigation Bar
    st.markdown("<br>" * 3, unsafe_allow_html=True)  # Space for bottom nav
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button("📊 Stats", key="nav_stats", help="View Statistics"):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col2:
        if st.button("📚 Learn", key="nav_edu", help="Educational Content"):
            st.session_state.active_tab = "Education"
            st.rerun()

    with col3:
        if st.button("🌤️ Weather", key="nav_weather", help="Weather Forecast"):
            st.session_state.active_tab = "Weather"
            st.rerun()

    with col4:
        if st.button("💰 Finance", key="nav_finance", help="Financial Services"):
            st.session_state.active_tab = "Finance"
            st.rerun()

    with col5:
        if st.button("👥 Network", key="nav_network", help="Stakeholder Network"):
            st.session_state.active_tab = "Network"
            st.rerun()

    with col6:
        if st.button("📰 News", key="nav_news", help="Industry News"):
            st.session_state.active_tab = "News"
            st.rerun()

if __name__ == "__main__":
    main()