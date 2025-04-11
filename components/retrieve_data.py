import streamlit as st
from services.authentication import (
    verify_passkey,
    handle_failed_attempt,
    reset_failed_attempts,
)
from services.storage import get_data_ids, get_encrypted_data
from services.encryption import decrypt_data
import time


def show_retrieve_data():
    """Display the retrieve data page"""
    st.subheader("Retrieve Your Data")

    current_user = st.session_state.current_user
    user_data = st.session_state.stored_data.get(current_user, {})

    # Show available data IDs
    if user_data:
        data_ids = get_data_ids()
        selected_id = st.selectbox("Select data to retrieve:", data_ids)

        with st.form("retrieve_data_form"):
            passkey = st.text_input("Enter Passkey:", type="password")
            submit_button = st.form_submit_button("Decrypt")

            if submit_button:
                if not passkey:
                    st.error("⚠️ Passkey is required!")
                else:
                    encrypted_data, stored_hash = get_encrypted_data(selected_id)

                    # Check if passkey is correct
                    if verify_passkey(passkey, stored_hash):
                        # Decrypt the data
                        decrypted_text = decrypt_data(encrypted_data, passkey)
                        if decrypted_text:
                            st.success("✅ Data decrypted successfully!")
                            st.code(decrypted_text)
                            reset_failed_attempts()
                        else:
                            st.error("⚠️ Decryption error. Contact administrator.")
                    else:
                        # Handle failed attempt
                        max_attempts_reached, message = handle_failed_attempt()
                        st.error(message)

                        if max_attempts_reached:
                            st.session_state.authorized = False
                            time.sleep(1)
                            st.rerun()
    else:
        st.warning("No encrypted data found. Please store some data first.")
