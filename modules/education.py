import streamlit as st

def show_content():
    st.header("Training and Education")
    
    module = st.selectbox(
        "Select Training Module",
        ["Basics of Poultry Farming",
         "Disease Management",
         "Feed Management",
         "Business Operations"]
    )
    
    if module == "Basics of Poultry Farming":
        st.subheader("Introduction to Poultry Farming")
        st.write("""
        1. Types of Poultry Birds
        2. Housing Requirements
        3. Basic Health Management
        4. Growth Stages
        """)
        
    elif module == "Disease Management":
        st.subheader("Common Diseases and Prevention")
        st.write("""
        1. Common Poultry Diseases
        2. Prevention Measures
        3. Vaccination Schedule
        4. Bio-security Measures
        """)
        
    elif module == "Feed Management":
        st.subheader("Feed Management")
        st.write("""
        1. Feed Types and Composition
        2. Feeding Schedule
        3. Water Management
        4. Feed Storage
        """)
        
    elif module == "Business Operations":
        st.subheader("Business Management")
        st.write("""
        1. Cost Management
        2. Marketing Strategies
        3. Record Keeping
        4. Supply Chain Management
        """)
