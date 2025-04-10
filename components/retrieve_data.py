import streamlit as st
from services.authentication import (
    is_locked_out,
    get_lockout_remaining,
    verify_passkey,
    handle_failed_attempt,
    reset_failed_attempts,
)
from services.storage import get_data_ids, get_encrypted_data
from services.encryption import decrypt_data


def show_retrieve_data():
    """Display the retrieve data page"""
    st.subheader("🔍 Retrieve Your Data")

    # Check if locked out due to previous failed attempts
    if is_locked_out():
        st.error(
            f"🔒 Account is temporarily locked. Please try again in {get_lockout_remaining()} seconds."
        )
    else:
        # Show available data IDs
        if st.session_state.stored_data:
            data_ids = get_data_ids()
            selected_id = st.selectbox("Select data to retrieve:", data_ids)

            with st.form("retrieve_data_form"):
                passkey = st.text_input("Enter Passkey:", type="password")
                submit_button = st.form_submit_button("Decrypt")

                if submit_button:
                    if not passkey:
                        st.error("⚠️ Passkey is required!")
                    else:
                        # Get the encrypted data
                        encrypted_data, stored_hash = get_encrypted_data(selected_id)

                        # Check if passkey is correct
                        if verify_passkey(passkey, stored_hash):
                            # Decrypt the data
                            decrypted_text = decrypt_data(encrypted_data, passkey)
                            if decrypted_text:
                                st.success("✅ Data decrypted successfully!")
                                st.code(decrypted_text)
                                # Reset failed attempts
                                reset_failed_attempts()
                            else:
                                st.error("⚠️ Decryption error. Contact administrator.")
                        else:
                            # Handle failed attempt
                            max_attempts_reached, message = handle_failed_attempt()
                            st.error(message)

                            if max_attempts_reached:
                                st.experimental_rerun()
        else:
            st.warning("No encrypted data found. Please store some data first.")
