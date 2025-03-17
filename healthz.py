import streamlit as st

def main():
    """Simple health check endpoint."""
    st.success("OK")
    st.stop()

if __name__ == "__main__":
    main() 