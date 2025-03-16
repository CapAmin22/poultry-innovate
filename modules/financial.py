import streamlit as st

def show_assistance():
    st.header("Bank Loan and Financial Assistance")
    
    st.subheader("Available Loan Schemes")
    
    schemes = {
        "NABARD Poultry Development": {
            "Max Amount": "₹50 Lakhs",
            "Interest Rate": "7-9%",
            "Tenure": "Up to 7 years"
        },
        "KCC for Poultry": {
            "Max Amount": "₹3 Lakhs",
            "Interest Rate": "4%",
            "Tenure": "Up to 5 years"
        },
        "MUDRA Loan": {
            "Max Amount": "₹10 Lakhs",
            "Interest Rate": "8-12%",
            "Tenure": "Up to 5 years"
        }
    }
    
    for scheme, details in schemes.items():
        with st.expander(scheme):
            for key, value in details.items():
                st.write(f"{key}: {value}")
    
    st.subheader("Required Documents")
    st.write("""
    - Identity Proof (Aadhaar/PAN)
    - Address Proof
    - Bank Statements (6 months)
    - Project Report
    - Land Documents
    - Experience Certificate (if any)
    """)
