import streamlit as st
from components.home import show_home
from components.store_data import show_store_data
from components.retrieve_data import show_retrieve_data
from components.login import show_login
from services.storage import load_data_from_file
from utils.session import initialize_session_state

# Initialize session state
initialize_session_state()

# Try to load data on app startup
try:
    load_data_from_file()
except:
    pass

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data"]
if not st.session_state.authorized:
    menu = ["Login"]

choice = st.sidebar.selectbox("Navigation", menu)

# Display the selected page
if choice == "Home":
    show_home()
elif choice == "Store Data" and st.session_state.authorized:
    show_store_data()
elif choice == "Retrieve Data" and st.session_state.authorized:
    show_retrieve_data()
elif choice == "Login" or not st.session_state.authorized:
    show_login()

# Show current status in sidebar
with st.sidebar:
    st.subheader("System Status")
    if st.session_state.authorized:
        st.success("🟢 Authorized")
    else:
        st.error("🔴 Locked - Reauthorization Required")

    # Display failed attempts if any
    if st.session_state.failed_attempts > 0:
        st.warning(f"Failed Attempts: {st.session_state.failed_attempts}/3")
