import streamlit as st
import pandas as pd

def show_directory():
    st.header("Networking for Stakeholders")

    # Directory filters
    category = st.selectbox(
        "Select Category",
        ["Farmers", "Feed Suppliers", "Equipment Manufacturers", "Veterinarians"]
    )

    state = st.selectbox(
        "Select State",
        ["All States", "Maharashtra", "Tamil Nadu", "Karnataka", "Telangana"]
    )

    # Display directory based on filters
    if category == "Farmers":
        show_farmers(state)
    elif category == "Feed Suppliers":
        show_suppliers(state)
    elif category == "Equipment Manufacturers":
        show_manufacturers(state)
    elif category == "Veterinarians":
        show_veterinarians(state)

def show_farmers(state):
    farmers = pd.DataFrame({
        "Name": ["Farmer 1", "Farmer 2", "Farmer 3"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Farm Size": ["Large", "Medium", "Small"],
        "Contact": ["contact1@email.com", "contact2@email.com", "contact3@email.com"]
    })

    if state != "All States":
        farmers = farmers[farmers["Location"] == state]

    st.dataframe(farmers)

def show_suppliers(state):
    suppliers = pd.DataFrame({
        "Name": ["Supplier 1", "Supplier 2", "Supplier 3"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Products": ["Feed Mix", "Grains", "Supplements"],
        "Contact": ["supplier1@email.com", "supplier2@email.com", "supplier3@email.com"]
    })

    if state != "All States":
        suppliers = suppliers[suppliers["Location"] == state]

    st.dataframe(suppliers)

def show_manufacturers(state):
    manufacturers = pd.DataFrame({
        "Name": ["Manufacturer 1", "Manufacturer 2", "Manufacturer 3"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Equipment": ["Feeders", "Incubators", "Ventilation"],
        "Contact": ["mfg1@email.com", "mfg2@email.com", "mfg3@email.com"]
    })

    if state != "All States":
        manufacturers = manufacturers[manufacturers["Location"] == state]

    st.dataframe(manufacturers)

def show_veterinarians(state):
    vets = pd.DataFrame({
        "Name": ["Dr. Smith", "Dr. Patel", "Dr. Kumar"],
        "Location": ["Maharashtra", "Tamil Nadu", "Karnataka"],
        "Specialization": ["Poultry Health", "Disease Control", "Nutrition"],
        "Contact": ["vet1@email.com", "vet2@email.com", "vet3@email.com"]
    })

    if state != "All States":
        vets = vets[vets["Location"] == state]

    st.dataframe(vets)