import json
import streamlit as st
from services.encryption import hash_passkey, encrypt_data


def save_data_to_file():
    """Save encrypted data to JSON file"""
    with open("encrypted_data.json", "w") as f:
        json.dump(st.session_state.stored_data, f)


def load_data_from_file():
    """Load encrypted data from JSON file"""
    try:
        with open("encrypted_data.json", "r") as f:
            st.session_state.stored_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.stored_data = {}


def store_new_data(user_id, user_data, passkey):
    """Store new encrypted data for current user"""
    current_user = st.session_state.current_user
    hashed_passkey = hash_passkey(passkey)
    encrypted_text = encrypt_data(user_data, passkey)

    # Initialize user data if not exists
    if current_user not in st.session_state.stored_data:
        st.session_state.stored_data[current_user] = {}

    # Store the encrypted data
    st.session_state.stored_data[current_user][user_id] = {
        "encrypted_text": encrypted_text,
        "passkey": hashed_passkey,
    }

    # Save to file
    try:
        save_data_to_file()
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False


def get_data_ids():
    """Get list of all stored data IDs for current user"""
    current_user = st.session_state.current_user
    if current_user in st.session_state.stored_data:
        return list(st.session_state.stored_data[current_user].keys())
    return []


def get_encrypted_data(data_id):
    """Get encrypted data and passkey hash for a specific ID for current user"""
    current_user = st.session_state.current_user
    if (
        current_user in st.session_state.stored_data
        and data_id in st.session_state.stored_data[current_user]
    ):
        return (
            st.session_state.stored_data[current_user][data_id]["encrypted_text"],
            st.session_state.stored_data[current_user][data_id]["passkey"],
        )
    return None, None
