import time
import json
import streamlit as st
from services.encryption import hash_passkey


def verify_passkey(passkey, stored_hash):
    """Verify if a passkey matches the stored hash"""
    return hash_passkey(passkey) == stored_hash


def handle_failed_attempt():
    """Handle a failed authentication attempt"""
    st.session_state.failed_attempts += 1

    # If current user exists, update their failed attempts in users dict
    if (
        st.session_state.current_user
        and st.session_state.current_user in st.session_state.users
    ):
        st.session_state.users[st.session_state.current_user][
            "failed_attempts"
        ] = st.session_state.failed_attempts
        save_users_to_file()

    remaining = 3 - st.session_state.failed_attempts
    if remaining > 0:
        return False, f"❌ Incorrect passkey! Attempts remaining: {remaining}"
    else:
        return True, "❌ Too many failed attempts! Logging out."


def reset_failed_attempts():
    """Reset the failed attempts counter"""
    st.session_state.failed_attempts = 0

    # If current user exists, reset their failed attempts in users dict
    if (
        st.session_state.current_user
        and st.session_state.current_user in st.session_state.users
    ):
        st.session_state.users[st.session_state.current_user]["failed_attempts"] = 0
        st.session_state.users[st.session_state.current_user]["last_failed_time"] = None
        save_users_to_file()


def username_exists(username):
    """Check if username already exists"""
    return username in st.session_state.users


def register_new_user(username, password):
    """Register a new user"""
    if username not in st.session_state.users:
        # Hash the password before storing
        hashed_password = hash_passkey(password)
        st.session_state.users[username] = {
            "password": hashed_password,
            "failed_attempts": 0,
            "last_failed_time": None,
        }
        save_users_to_file()
        return True
    return False


def verify_user_credentials(username, password):
    """Verify username and password"""
    if username in st.session_state.users:
        stored_hash = st.session_state.users[username]["password"]
        if hash_passkey(password) == stored_hash:
            # Transfer user's failed attempts to session state
            st.session_state.failed_attempts = st.session_state.users[username][
                "failed_attempts"
            ]
            st.session_state.last_failed_time = st.session_state.users[username][
                "last_failed_time"
            ]
            return True
    return False


def handle_failed_login_attempt(username):
    """Handle a failed login attempt for a specific user"""
    if username in st.session_state.users:
        st.session_state.users[username]["failed_attempts"] += 1
        st.session_state.users[username]["last_failed_time"] = time.time()
        st.session_state.failed_attempts = st.session_state.users[username][
            "failed_attempts"
        ]
        st.session_state.last_failed_time = st.session_state.users[username][
            "last_failed_time"
        ]
        save_users_to_file()


def save_users_to_file():
    """Save user data to file"""
    try:
        with open("users.json", "w") as f:
            json.dump(st.session_state.users, f)
    except Exception as e:
        st.error(f"Error saving user data: {e}")


def load_users_from_file():
    """Load user data from file"""
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def verify_master_password(password):
    """Verify the master password for reauthorization - only for admin purposes"""
    # This is for compatibility with the original system's admin override
    # In a real multi-user system, this would use a different authentication method
    return password == "admin123"
