import streamlit as st
import pandas as pd
from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)

# Dummy data for demonstration
DUMMY_USERS = {
    "john.doe": {
        "name": "John Doe",
        "title": "Poultry Farm Manager",
        "company": "Green Fields Poultry",
        "location": "Manila, Philippines",
        "bio": "20+ years experience in poultry farm management",
        "connections": ["sarah.smith", "mike.jones", "anna.wilson"],
        "image": "👨‍🌾"
    },
    "sarah.smith": {
        "name": "Sarah Smith",
        "title": "Veterinary Specialist",
        "company": "PetCare Plus",
        "location": "Cebu, Philippines",
        "bio": "Specialized in poultry health and disease prevention",
        "connections": ["john.doe", "anna.wilson"],
        "image": "👩‍⚕️"
    }
}

DUMMY_POSTS = [
    {
        "id": 1,
        "author": "john.doe",
        "content": "Just implemented a new feeding system that improved efficiency by 25%! #PoultryInnovation",
        "timestamp": "2024-03-17 09:30:00",
        "likes": 15,
        "comments": [
            {"user": "sarah.smith", "content": "Great results! Would love to learn more about your system."}
        ]
    }
]

def init_session_state():
    """Initialize session state variables."""
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "username": "guest",
            "logged_in": False
        }
    if "posts" not in st.session_state:
        st.session_state.posts = DUMMY_POSTS
    if "users" not in st.session_state:
        st.session_state.users = DUMMY_USERS
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = None

def show_profile(username):
    """Display user profile in a card format."""
    user = st.session_state.users.get(username)
    if not user:
        st.error("User not found")
        return

    with st.container():
        st.markdown(f"""
        <div class="modern-card" style="padding: 2rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 3rem;">{user['image']}</div>
                <div>
                    <h2 style="margin: 0;">{user['name']}</h2>
                    <p style="margin: 0; color: #666;">{user['title']} at {user['company']}</p>
                    <p style="margin: 0; color: #666;">{user['location']}</p>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <p>{user['bio']}</p>
                <p><strong>{len(user['connections'])}</strong> connections</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_post():
    """Create a new post interface."""
    with st.form("create_post"):
        content = st.text_area("Share your thoughts", max_chars=1000)
        submitted = st.form_submit_button("Post")
        
        if submitted and content:
            new_post = {
                "id": len(st.session_state.posts) + 1,
                "author": st.session_state.user_profile["username"],
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "likes": 0,
                "comments": []
            }
            st.session_state.posts.insert(0, new_post)
            st.success("Post created successfully!")
            st.rerun()

def show_post(post):
    """Display a single post in card format."""
    author = st.session_state.users.get(post["author"], {"name": "Unknown User", "image": "👤"})
    
    with st.container():
        st.markdown(f"""
        <div class="modern-card" style="padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{author['image']}</span>
                <strong>{author['name']}</strong>
            </div>
            <p style="margin: 0.5rem 0;">{post['content']}</p>
            <div style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">
                {post['timestamp']} • {post['likes']} likes • {len(post['comments'])} comments
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Like and comment buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Like", key=f"like_{post['id']}"):
                post["likes"] += 1
                st.rerun()
        with col2:
            if st.button("💬 Comment", key=f"comment_{post['id']}"):
                st.text_input("Add a comment", key=f"comment_input_{post['id']}")

def show_chat():
    """Display chat interface."""
    st.markdown("### Messages")
    
    # Contact list
    selected_contact = st.selectbox(
        "Select contact",
        options=[user["name"] for user in st.session_state.users.values()],
        key="chat_contact"
    )
    
    # Chat interface
    st.markdown(f"""
    <div class="modern-card" style="height: 300px; overflow-y: auto; padding: 1rem; margin: 1rem 0;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <div style="align-self: flex-end; background: #00ff87; color: #1a1c2b; padding: 0.5rem; border-radius: 10px;">
                Hey, how's your farm doing?
            </div>
            <div style="align-self: flex-start; background: rgba(255,255,255,0.1); padding: 0.5rem; border-radius: 10px;">
                Great! Just implemented new feeding system.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Message input
    with st.form("send_message"):
        message = st.text_input("Type your message")
        if st.form_submit_button("Send"):
            st.success("Message sent!")

def show_collaboration_module():
    """Main collaboration module display."""
    st.markdown("## Collaboration Hub")
    
    init_session_state()
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["Feed", "Network", "Messages"])
    
    with tab1:
        st.markdown("### Share Updates")
        create_post()
        
        st.markdown("### Recent Posts")
        for post in st.session_state.posts:
            show_post(post)
    
    with tab2:
        st.markdown("### Your Network")
        
        # Search and filters
        st.text_input("Search connections", placeholder="Search by name or company")
        
        # Display connections
        for username, user in st.session_state.users.items():
            if username != st.session_state.user_profile["username"]:
                show_profile(username)
    
    with tab3:
        show_chat()

if __name__ == "__main__":
    st.set_page_config(page_title="Collaboration Hub", layout="wide")
    show_collaboration_module() 