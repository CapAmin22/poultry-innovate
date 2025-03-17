import streamlit as st
import pandas as pd
from datetime import datetime
import logging
import random
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Enhanced dummy data
DUMMY_USERS = {
    "john.doe": {
        "name": "John Doe",
        "title": "Poultry Farm Manager",
        "company": "Green Fields Poultry",
        "location": "Manila, Philippines",
        "bio": "20+ years experience in poultry farm management. Specializing in sustainable farming practices and modern poultry technology.",
        "connections": ["sarah.smith", "mike.jones", "anna.wilson"],
        "pending_connections": [],
        "image": "👨‍🌾",
        "skills": ["Farm Management", "Poultry Health", "Sustainable Practices"],
        "experience": [
            {
                "title": "Farm Manager",
                "company": "Green Fields Poultry",
                "duration": "2018 - Present"
            },
            {
                "title": "Assistant Manager",
                "company": "Golden Eggs Farm",
                "duration": "2015 - 2018"
            }
        ]
    },
    "sarah.smith": {
        "name": "Sarah Smith",
        "title": "Veterinary Specialist",
        "company": "PetCare Plus",
        "location": "Cebu, Philippines",
        "bio": "Specialized in poultry health and disease prevention. Passionate about implementing innovative healthcare solutions.",
        "connections": ["john.doe", "anna.wilson"],
        "pending_connections": [],
        "image": "👩‍⚕️",
        "skills": ["Veterinary Medicine", "Disease Prevention", "Animal Welfare"],
        "experience": [
            {
                "title": "Lead Veterinarian",
                "company": "PetCare Plus",
                "duration": "2019 - Present"
            }
        ]
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
        ],
        "image": None
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
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = {}
    if "notifications" not in st.session_state:
        st.session_state.notifications = []

def show_connection_status(username: str) -> None:
    """Display connection status and handle connection requests."""
    current_user = st.session_state.user_profile["username"]
    user = st.session_state.users[username]
    
    if username == current_user:
        return
        
    if username in st.session_state.users[current_user]["connections"]:
        st.button("✓ Connected", key=f"connected_{username}", disabled=True)
    elif username in st.session_state.users[current_user]["pending_connections"]:
        st.button("Pending", key=f"pending_{username}", disabled=True)
    else:
        if st.button("Connect", key=f"connect_{username}"):
            st.session_state.users[current_user]["pending_connections"].append(username)
            st.session_state.notifications.append({
                "title": "Connection Request",
                "message": f"{st.session_state.users[current_user]['name']} sent you a connection request",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.rerun()

def show_profile(username: str, show_full: bool = False):
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
                <div style="flex-grow: 1;">
                    <h2 style="margin: 0;">{user['name']}</h2>
                    <p style="margin: 0; opacity: 0.8;">{user['title']} at {user['company']}</p>
                    <p style="margin: 0; opacity: 0.8;">{user['location']}</p>
                </div>
                <div>
        """, unsafe_allow_html=True)
        
        show_connection_status(username)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if show_full:
            st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <h3>About</h3>
                    <p>{user['bio']}</p>
                    
                    <h3>Skills</h3>
                    <p>{', '.join(user['skills'])}</p>
                    
                    <h3>Experience</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for exp in user['experience']:
                st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <strong>{exp['title']}</strong><br>
                        {exp['company']}<br>
                        <small>{exp['duration']}</small>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="margin-top: 1rem;">
                <p><strong>{len(user['connections'])}</strong> connections</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_post():
    """Create a new post interface."""
    with st.form("create_post"):
        content = st.text_area("Share your thoughts", max_chars=1000, 
                             placeholder="What's on your mind? Share updates, insights, or questions...")
        image = st.file_uploader("Add an image", type=["png", "jpg", "jpeg"])
        col1, col2 = st.columns([1, 5])
        with col1:
            submitted = st.form_submit_button("Post")
        
        if submitted and content:
            new_post = {
                "id": len(st.session_state.posts) + 1,
                "author": st.session_state.user_profile["username"],
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "likes": 0,
                "comments": [],
                "image": image.name if image else None
            }
            st.session_state.posts.insert(0, new_post)
            st.success("Post created successfully!")
            st.rerun()

def show_post(post: Dict, show_interactions: bool = True):
    """Display a single post in card format."""
    author = st.session_state.users.get(post["author"], {"name": "Unknown User", "image": "👤"})
    
    with st.container():
        st.markdown(f"""
        <div class="modern-card" style="padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; cursor: pointer;">
                <span style="font-size: 1.5rem;">{author['image']}</span>
                <div>
                    <strong>{author['name']}</strong><br>
                    <small style="opacity: 0.8;">{author['title']} at {author['company']}</small>
                </div>
            </div>
            <p style="margin: 0.5rem 0;">{post['content']}</p>
            """, unsafe_allow_html=True)
        
        if post.get("image"):
            st.image(post["image"], use_column_width=True)
        
        st.markdown(f"""
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.5rem;">
                {post['timestamp']} • {post['likes']} likes • {len(post['comments'])} comments
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_interactions:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Like", key=f"like_{post['id']}"):
                    post["likes"] += 1
                    st.rerun()
            with col2:
                if st.button("💬 Comment", key=f"comment_{post['id']}"):
                    comment = st.text_input("Add a comment", key=f"comment_input_{post['id']}")
                    if comment:
                        post["comments"].append({
                            "user": st.session_state.user_profile["username"],
                            "content": comment
                        })
                        st.rerun()
            with col3:
                if st.button("↗ Share", key=f"share_{post['id']}"):
                    st.success("Post shared!")

def show_chat():
    """Display chat interface."""
    st.markdown("### Messages")
    
    # Contact list with search
    st.text_input("Search contacts", key="contact_search", placeholder="Type to search...")
    search_term = st.session_state.get("contact_search", "").lower()
    
    # Filter contacts based on search
    contacts = [
        user for username, user in st.session_state.users.items()
        if username in st.session_state.users[st.session_state.user_profile["username"]]["connections"]
        and (search_term in user["name"].lower() or search_term in user["title"].lower())
    ]
    
    # Display contacts
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Contacts")
        for user in contacts:
            if st.button(
                f"{user['image']} {user['name']}",
                key=f"chat_{user['name']}",
                use_container_width=True
            ):
                st.session_state.active_chat = user["name"]
                st.rerun()
    
    with col2:
        if st.session_state.active_chat:
            active_user = next(user for user in contacts if user["name"] == st.session_state.active_chat)
            st.markdown(f"#### Chat with {active_user['name']}")
            
            # Chat container
            chat_container = st.container()
            with chat_container:
                st.markdown("""
                <div class="modern-card" style="height: 300px; overflow-y: auto; padding: 1rem;">
                    <div class="chat-messages" style="display: flex; flex-direction: column; gap: 0.5rem;">
                """, unsafe_allow_html=True)
                
                # Display messages
                chat_id = f"{st.session_state.user_profile['username']}_{active_user['name']}"
                messages = st.session_state.chat_messages.get(chat_id, [])
                
                for msg in messages:
                    alignment = "flex-end" if msg["sender"] == st.session_state.user_profile["username"] else "flex-start"
                    bg_color = "#00ff87" if msg["sender"] == st.session_state.user_profile["username"] else "rgba(255,255,255,0.1)"
                    text_color = "#1a1c2b" if msg["sender"] == st.session_state.user_profile["username"] else "#ffffff"
                    
                    st.markdown(f"""
                        <div style="align-self: {alignment}; background: {bg_color}; color: {text_color}; 
                                padding: 0.5rem; border-radius: 10px; max-width: 80%;">
                            {msg['content']}
                            <br><small style="opacity: 0.7;">{msg['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Message input
            with st.form("send_message", clear_on_submit=True):
                message = st.text_input("Type your message", key="message_input")
                if st.form_submit_button("Send"):
                    if message:
                        if chat_id not in st.session_state.chat_messages:
                            st.session_state.chat_messages[chat_id] = []
                        
                        st.session_state.chat_messages[chat_id].append({
                            "sender": st.session_state.user_profile["username"],
                            "content": message,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        st.rerun()

def show_collaboration_module():
    """Main collaboration module display."""
    st.markdown("## Collaboration Hub")
    
    init_session_state()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Feed", "Network", "Messages", "My Profile"])
    
    with tab1:
        st.markdown("### Share Updates")
        create_post()
        
        st.markdown("### Recent Posts")
        for post in st.session_state.posts:
            show_post(post)
    
    with tab2:
        st.markdown("### Your Network")
        
        # Search and filters
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("Search connections", placeholder="Search by name, company, or location")
        with col2:
            filter_option = st.selectbox("Filter by", ["All", "Connected", "Pending"])
        
        # Display connections
        for username, user in st.session_state.users.items():
            if username != st.session_state.user_profile["username"]:
                if (not search or 
                    search.lower() in user["name"].lower() or 
                    search.lower() in user["company"].lower() or
                    search.lower() in user["location"].lower()):
                    show_profile(username)
    
    with tab3:
        show_chat()
    
    with tab4:
        st.markdown("### My Profile")
        show_profile(st.session_state.user_profile["username"], show_full=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Collaboration Hub", layout="wide")
    show_collaboration_module() 