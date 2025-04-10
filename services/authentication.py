import time
import streamlit as st
from services.encryption import hash_passkey


def is_locked_out():
    """Check if user is locked out due to too many failed attempts"""
    if st.session_state.last_failed_time is not None:
        time_diff = time.time() - st.session_state.last_failed_time
        if time_diff < 30:  # 30-second lockout
            return True
    return False


def get_lockout_remaining():
    """Get remaining lockout time in seconds"""
    if st.session_state.last_failed_time is not None:
        time_diff = time.time() - st.session_state.last_failed_time
        if time_diff < 30:
            return int(30 - time_diff)
    return 0


def verify_passkey(passkey, stored_hash):
    """Verify if a passkey matches the stored hash"""
    return hash_passkey(passkey) == stored_hash


def handle_failed_attempt():
    """Handle a failed authentication attempt"""
    st.session_state.failed_attempts += 1
    st.session_state.last_failed_time = time.time()

    remaining = 3 - st.session_state.failed_attempts
    if remaining > 0:
        return False, f"❌ Incorrect passkey! Attempts remaining: {remaining}"
    else:
        st.session_state.authorized = False
        return True, "❌ Too many failed attempts!"


def reset_failed_attempts():
    """Reset the failed attempts counter"""
    st.session_state.failed_attempts = 0


def verify_master_password(password):
    """Verify the master password for reauthorization"""
    # For demo purposes - replace with proper authentication
    return password == "admin123"
