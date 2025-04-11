import streamlit as st
from services.storage import store_new_data


def show_store_data():
    """Display the store data page"""
    st.subheader("📂 Store Data Securely")

    with st.form("store_data_form"):
        user_id = st.text_input("Enter a unique ID for this data:")
        user_data = st.text_area("Enter Data to Encrypt:")
        passkey = st.text_input("Create a Passkey:", type="password")
        confirm_passkey = st.text_input("Confirm Passkey:", type="password")

        submit_button = st.form_submit_button("Encrypt & Save")

        if submit_button:
            if not user_id or not user_data or not passkey:
                st.error("⚠️ All fields are required!")
            elif passkey != confirm_passkey:
                st.error("⚠️ Passkeys do not match!")
            elif user_id in st.session_state.stored_data.get(
                st.session_state.current_user, {}
            ):
                st.error("⚠️ This ID already exists. Please use a different ID.")
            else:
                success = store_new_data(user_id, user_data, passkey)
                if success:
                    st.success(f"✅ Data stored securely with ID: {user_id}")
                    st.info(
                        "Make sure to remember your passkey - it cannot be recovered!"
                    )
                else:
                    st.error("⚠️ Failed to save data. Please try again.")
