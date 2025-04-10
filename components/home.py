import streamlit as st


def show_home():
    """Display the home page"""
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write(
        "Use this app to **securely store and retrieve data** using unique passkeys."
    )

    st.info(
        """
    **How it works:**
    1. **Store Data**: Enter your text and create a unique passkey
    2. **Retrieve Data**: Use your passkey to decrypt and view your data
    3. **Security**: After 3 failed attempts, you'll need to reauthorize
    """
    )

    # Display number of encrypted items
    st.metric("Encrypted Items Stored", len(st.session_state.stored_data))
