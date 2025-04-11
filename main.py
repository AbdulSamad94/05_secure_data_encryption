import streamlit as st
from components.home import show_home
from components.store_data import show_store_data
from components.retrieve_data import show_retrieve_data
from components.login import show_login
from components.register import show_register
from services.storage import load_data_from_file
from services.authentication import load_users_from_file
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

# Show login or register page if not authorized
if not st.session_state.authorized:
    if st.session_state.show_register:
        show_register()
    else:
        show_login()
else:
    # Navigation for authenticated users
    menu = ["Home", "Store Data", "Retrieve Data"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # Display the selected page
    if choice == "Home":
        show_home()
    elif choice == "Store Data":
        show_store_data()
    elif choice == "Retrieve Data":
        show_retrieve_data()

    # Show current status in sidebar
    with st.sidebar:
        st.subheader("User Information")
        st.success(f"🟢 Logged in as: {st.session_state.current_user}")

        # Logout button
        if st.button("Logout"):
            st.session_state.authorized = False
            st.session_state.current_user = None
            st.session_state.show_login = True
            st.experimental_rerun()

        st.subheader("System Status")
        if st.session_state.failed_attempts > 0:
            st.warning(f"Failed Attempts: {st.session_state.failed_attempts}/3")
