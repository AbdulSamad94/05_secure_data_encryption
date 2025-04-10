import streamlit as st
from cryptography.fernet import Fernet


def initialize_session_state():
    """Initialize all session state variables"""

    # Data storage
    if "stored_data" not in st.session_state:
        st.session_state.stored_data = {}

    # Authentication state
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0

    if "last_failed_time" not in st.session_state:
        st.session_state.last_failed_time = None

    if "authorized" not in st.session_state:
        st.session_state.authorized = True

    # Encryption key
    if "key" not in st.session_state:
        st.session_state.key = Fernet.generate_key()
        st.session_state.cipher = Fernet(st.session_state.key)
