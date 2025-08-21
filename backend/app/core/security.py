import base64
from cryptography.fernet import Fernet
from .config import SECRET_KEY

try:
    # Fernet requires a 32-byte key, URL-safe and base64-encoded.
    # We derive a valid key from the SECRET_KEY in the config.
    padded_key = SECRET_KEY.ljust(32)
    final_key = padded_key[:32].encode('utf-8')
    encoded_key = base64.urlsafe_b64encode(final_key)
    cipher_suite = Fernet(encoded_key)
except Exception as e:
    print(f"CRITICAL: Failed to initialize encryption suite. Ensure SECRET_KEY is set correctly. Error: {e}")
    cipher_suite = None

def encrypt_password(password: str) -> str:
    """
    Encrypts a password using Fernet symmetric encryption.
    """
    if not cipher_suite:
        raise ValueError("Encryption service is not available.")

    encrypted_bytes = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_password(encrypted_password: str) -> str:
    """
    Decrypts an encrypted password string.
    """
    if not cipher_suite:
        raise ValueError("Encryption service is not available.")

    decrypted_bytes = cipher_suite.decrypt(encrypted_password.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')
