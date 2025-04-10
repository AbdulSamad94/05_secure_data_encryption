import streamlit as st
import time
from services.authentication import (
    is_locked_out,
    get_lockout_remaining,
    verify_master_password,
)


def show_login():
    """Display the login/reauthorization page"""
    st.subheader("🔑 Authorization Required")

    if is_locked_out():
        st.error(
            f"🔒 Account is temporarily locked. Please try again in {get_lockout_remaining()} seconds."
        )
    else:
        with st.form("login_form"):
            st.write("You've been locked out due to too many failed attempts.")
            login_pass = st.text_input(
                "Enter Master Password to continue:", type="password"
            )
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if verify_master_password(login_pass):
                    st.session_state.failed_attempts = 0
                    st.session_state.authorized = True
                    st.success("✅ Authentication successful!")
                    time.sleep(1)  # Short delay for the success message to show
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect password!")
