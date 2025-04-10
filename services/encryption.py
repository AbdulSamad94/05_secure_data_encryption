import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def hash_passkey(passkey):
    """Hash a passkey using SHA-256"""
    return hashlib.sha256(passkey.encode()).hexdigest()


def derive_key(passkey, salt=None):
    """Derive a key from passkey using PBKDF2 (more secure)"""
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


def encrypt_data(text, passkey):
    """Encrypt data using a unique key derived from the passkey"""
    unique_key = derive_key(passkey)
    cipher = Fernet(unique_key)
    return cipher.encrypt(text.encode()).decode()


def decrypt_data(encrypted_text, passkey):
    """Decrypt data using a unique key derived from the passkey"""
    try:
        unique_key = derive_key(passkey)
        cipher = Fernet(unique_key)
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception:
        return None
