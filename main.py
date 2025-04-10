import streamlit as st
import hashlib
import base64
import json
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Session state initialization
if "stored_data" not in st.session_state:
    st.session_state.stored_data = (
        {}
    )  # {"unique_id": {"encrypted_text": "xyz", "passkey": "hashed"}}

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "last_failed_time" not in st.session_state:
    st.session_state.last_failed_time = None

if "key" not in st.session_state:
    # Generate a key for Fernet encryption
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

if "authorized" not in st.session_state:
    st.session_state.authorized = True


# Function to hash passkey with SHA-256
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()


# Function to derive a key from passkey using PBKDF2 (more secure)
def derive_key(passkey, salt=None):
    if salt is None:
        salt = b"secure_salt_value"  # In production, use a random salt per user and store it

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passkey.encode()))
    return key


# Function to encrypt data
def encrypt_data(text, passkey):
    # Generate a unique cipher for this specific encryption
    unique_key = derive_key(passkey)
    cipher = Fernet(unique_key)
    return cipher.encrypt(text.encode()).decode()


# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    try:
        unique_key = derive_key(passkey)
        cipher = Fernet(unique_key)
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception:
        return None


# Function to check if user is locked out
def is_locked_out():
    if st.session_state.last_failed_time is not None:
        time_diff = time.time() - st.session_state.last_failed_time
        if time_diff < 30:  # 30-second lockout
            return True
    return False


# Function to get remaining lockout time
def get_lockout_remaining():
    if st.session_state.last_failed_time is not None:
        time_diff = time.time() - st.session_state.last_failed_time
        if time_diff < 30:
            return int(30 - time_diff)
    return 0


# Save data to JSON file (persistence challenge)
def save_data_to_file():
    with open("encrypted_data.json", "w") as f:
        json.dump(st.session_state.stored_data, f)


# Load data from JSON file
def load_data_from_file():
    try:
        with open("encrypted_data.json", "r") as f:
            st.session_state.stored_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.stored_data = {}


# Try to load data on app startup
try:
    load_data_from_file()
except:
    pass

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data"]
if not st.session_state.authorized:
    menu = ["Login"]

choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
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

elif choice == "Store Data" and st.session_state.authorized:
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
            elif user_id in st.session_state.stored_data:
                st.error("⚠️ This ID already exists. Please use a different ID.")
            else:
                hashed_passkey = hash_passkey(passkey)
                encrypted_text = encrypt_data(user_data, passkey)

                # Store the encrypted data
                st.session_state.stored_data[user_id] = {
                    "encrypted_text": encrypted_text,
                    "passkey": hashed_passkey,
                }

                # Save to file (persistence challenge)
                try:
                    save_data_to_file()
                except:
                    pass

                st.success(f"✅ Data stored securely with ID: {user_id}")
                st.info("Make sure to remember your passkey - it cannot be recovered!")

elif choice == "Retrieve Data" and st.session_state.authorized:
    st.subheader("🔍 Retrieve Your Data")

    # Check if locked out due to previous failed attempts
    if is_locked_out():
        st.error(
            f"🔒 Account is temporarily locked. Please try again in {get_lockout_remaining()} seconds."
        )
    else:
        # Show available data IDs
        if st.session_state.stored_data:
            data_ids = list(st.session_state.stored_data.keys())
            selected_id = st.selectbox("Select data to retrieve:", data_ids)

            with st.form("retrieve_data_form"):
                passkey = st.text_input("Enter Passkey:", type="password")
                submit_button = st.form_submit_button("Decrypt")

                if submit_button:
                    if not passkey:
                        st.error("⚠️ Passkey is required!")
                    else:
                        # Get the encrypted data
                        encrypted_data = st.session_state.stored_data[selected_id][
                            "encrypted_text"
                        ]
                        stored_hash = st.session_state.stored_data[selected_id][
                            "passkey"
                        ]

                        # Check if passkey is correct
                        if hash_passkey(passkey) == stored_hash:
                            # Decrypt the data
                            decrypted_text = decrypt_data(encrypted_data, passkey)
                            if decrypted_text:
                                st.success("✅ Data decrypted successfully!")
                                st.code(decrypted_text)
                                # Reset failed attempts
                                st.session_state.failed_attempts = 0
                            else:
                                st.error("⚠️ Decryption error. Contact administrator.")
                        else:
                            # Increment failed attempts
                            st.session_state.failed_attempts += 1
                            st.session_state.last_failed_time = time.time()

                            remaining = 3 - st.session_state.failed_attempts
                            if remaining > 0:
                                st.error(
                                    f"❌ Incorrect passkey! Attempts remaining: {remaining}"
                                )
                            else:
                                st.error("❌ Too many failed attempts!")
                                st.session_state.authorized = False
                                st.experimental_rerun()
        else:
            st.warning("No encrypted data found. Please store some data first.")

elif choice == "Login" or not st.session_state.authorized:
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
                # For demo purposes - replace with proper authentication
                if login_pass == "admin123":
                    st.session_state.failed_attempts = 0
                    st.session_state.authorized = True
                    st.success("✅ Authentication successful!")
                    time.sleep(1)  # Short delay for the success message to show
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect password!")

# Show current status in sidebar
with st.sidebar:
    st.subheader("System Status")
    if st.session_state.authorized:
        st.success("🟢 Authorized")
    else:
        st.error("🔴 Locked - Reauthorization Required")

    # Display failed attempts if any
    if st.session_state.failed_attempts > 0:
        st.warning(f"Failed Attempts: {st.session_state.failed_attempts}/3")
