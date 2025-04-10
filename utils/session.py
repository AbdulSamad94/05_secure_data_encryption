import streamlit as st
from cryptography.fernet import Fernet
from services.authentication import load_users_from_file


def initialize_session_state():
    """Initialize all session state variables"""

    # Data storage
    if "stored_data" not in st.session_state:
        st.session_state.stored_data = {}

    # User storage
    if "users" not in st.session_state:
        st.session_state.users = load_users_from_file()

    # Authentication state
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0

    if "authorized" not in st.session_state:
        st.session_state.authorized = False

    if "current_user" not in st.session_state:
        st.session_state.current_user = None

    # UI flow control
    if "show_login" not in st.session_state:
        st.session_state.show_login = True

    if "show_register" not in st.session_state:
        st.session_state.show_register = False

    # Encryption key
    if "key" not in st.session_state:
        st.session_state.key = Fernet.generate_key()
        st.session_state.cipher = Fernet(st.session_state.key)
