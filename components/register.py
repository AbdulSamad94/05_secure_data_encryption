import streamlit as st
import time
from services.authentication import register_new_user, username_exists


def show_register():
    """Display the registration page"""
    st.subheader("Register New Account")

    with st.form("register_form"):
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")

        submit_button = st.form_submit_button("Register")

        if submit_button:
            if not username or not password:
                st.error("⚠️ All fields are required!")
            elif len(password) < 8:
                st.error("⚠️ Password must be at least 8 characters long!")
            elif password != confirm_password:
                st.error("⚠️ Passwords do not match!")
            elif username_exists(username):
                st.error("⚠️ Username already exists!")
            else:
                if register_new_user(username, password):
                    st.success("✅ Registration successful! Please log in.")
                    time.sleep(1)
                    st.session_state.show_login = True
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error("⚠️ Registration failed. Please try again.")

    # Back to login button
    if st.button("Already have an account? Login here"):
        st.session_state.show_register = False
        st.session_state.show_login = True
        st.rerun()
