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
    """Store new encrypted data"""
    hashed_passkey = hash_passkey(passkey)
    encrypted_text = encrypt_data(user_data, passkey)

    # Store the encrypted data
    st.session_state.stored_data[user_id] = {
        "encrypted_text": encrypted_text,
        "passkey": hashed_passkey,
    }

    # Save to file
    try:
        save_data_to_file()
        return True
    except:
        return False


def get_data_ids():
    """Get list of all stored data IDs"""
    return list(st.session_state.stored_data.keys())


def get_encrypted_data(data_id):
    """Get encrypted data and passkey hash for a specific ID"""
    if data_id in st.session_state.stored_data:
        return (
            st.session_state.stored_data[data_id]["encrypted_text"],
            st.session_state.stored_data[data_id]["passkey"],
        )
    return None, None
