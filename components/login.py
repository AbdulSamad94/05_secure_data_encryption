import streamlit as st
import time
from services.authentication import (
    verify_user_credentials,
    handle_failed_login_attempt,
)


def show_login():
    """Display the login page"""
    st.subheader("🔑 Login")

    with st.form("login_form"):
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not username or not password:
                st.error("⚠️ All fields are required!")
            elif verify_user_credentials(username, password):
                st.session_state.failed_attempts = 0
                st.session_state.authorized = True
                st.session_state.current_user = username
                st.success("✅ Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
                handle_failed_login_attempt(username)

    if st.button("Don't have an account? Register here"):
        st.session_state.show_register = True
        st.session_state.show_login = False
        st.rerun()
