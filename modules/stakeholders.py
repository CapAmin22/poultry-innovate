import streamlit as st
import pandas as pd

def show_directory():
    st.markdown("""
    <h1 style='text-align: center; color: #333; font-size: 2rem; margin-bottom: 2rem;'>
        👥 Stakeholder Network
    </h1>
    """, unsafe_allow_html=True)

    # Modern filter section
    st.markdown("""
    <style>
    .filter-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .stSelectbox {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-container">', unsafe_allow_html=True)

    # Directory filters with icons
    category = st.selectbox(
        "🔍 Select Category",
        ["Farmers", "Feed Suppliers", "Equipment Manufacturers", "Veterinarians"]
    )

    state = st.selectbox(
        "📍 Select State",
        ["All States", "Maharashtra", "Tamil Nadu", "Karnataka", "Telangana"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Custom styling for cards
    st.markdown("""
    <style>
    .stakeholder-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .stakeholder-card:hover {
        transform: translateY(-2px);
    }
    .contact-button {
        background-color: #ff4b4b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display directory based on filters
    if category == "Farmers":
        show_farmers(state)
    elif category == "Feed Suppliers":
        show_suppliers(state)
    elif category == "Equipment Manufacturers":
        show_manufacturers(state)
    elif category == "Veterinarians":
        show_veterinarians(state)

def create_contact_card(data):
    """Helper function to create a consistent contact card layout"""
    st.markdown(f"""
    <div class="stakeholder-card">
        <h3>{data['Name']}</h3>
        <p>📍 {data['Location']}</p>
        <p>{get_icon_for_category(data)} {get_details_text(data)}</p>
        <a href="mailto:{data['Contact']}" class="contact-button">
            ✉️ Contact
        </a>
    </div>
    """, unsafe_allow_html=True)

def get_icon_for_category(data):
    if 'Farm Size' in data:
        return "🚜"
    elif 'Products' in data:
        return "🌾"
    elif 'Equipment' in data:
        return "⚙️"
    elif 'Specialization' in data:
        return "👨‍⚕️"
    return "📋"

def get_details_text(data):
    if 'Farm Size' in data:
        return f"Farm Size: {data['Farm Size']}"
    elif 'Products' in data:
        return f"Products: {data['Products']}"
    elif 'Equipment' in data:
        return f"Equipment: {data['Equipment']}"
    elif 'Specialization' in data:
        return f"Specialization: {data['Specialization']}"
    return ""

def show_farmers(state):
    farmers = pd.DataFrame({
        "Name": ["Farmer 1", "Farmer 2", "Farmer 3"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Farm Size": ["Large", "Medium", "Small"],
        "Contact": ["contact1@email.com", "contact2@email.com", "contact3@email.com"]
    })

    if state != "All States":
        farmers = farmers[farmers["Location"] == state]

    for _, farmer in farmers.iterrows():
        create_contact_card(farmer)

def show_suppliers(state):
    suppliers = pd.DataFrame({
        "Name": ["Supplier 1", "Supplier 2", "Supplier 3"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Products": ["Feed Mix", "Grains", "Supplements"],
        "Contact": ["supplier1@email.com", "supplier2@email.com", "supplier3@email.com"]
    })

    if state != "All States":
        suppliers = suppliers[suppliers["Location"] == state]

    for _, supplier in suppliers.iterrows():
        create_contact_card(supplier)

def show_manufacturers(state):
    manufacturers = pd.DataFrame({
        "Name": ["Manufacturer 1", "Manufacturer 2", "Manufacturer 3"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Equipment": ["Feeders", "Incubators", "Ventilation"],
        "Contact": ["mfg1@email.com", "mfg2@email.com", "mfg3@email.com"]
    })

    if state != "All States":
        manufacturers = manufacturers[manufacturers["Location"] == state]

    for _, manufacturer in manufacturers.iterrows():
        create_contact_card(manufacturer)

def show_veterinarians(state):
    vets = pd.DataFrame({
        "Name": ["Dr. Smith", "Dr. Patel", "Dr. Kumar"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Specialization": ["Poultry Health", "Disease Control", "Nutrition"],
        "Contact": ["vet1@email.com", "vet2@email.com", "vet3@email.com"]
    })

    if state != "All States":
        vets = vets[vets["Location"] == state]

    for _, vet in vets.iterrows():
        create_contact_card(vet)