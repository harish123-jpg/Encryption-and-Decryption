import base64

from cryptography.fernet import Fernet


def generate_key():
    """Generate a new encryption key."""
    key = Fernet.generate_key()
    return key


def encrypt_file(file_content, key):
    """Encrypt file content using the provided key."""
    cipher = Fernet(key)
    encrypted_content = cipher.encrypt(file_content)
    return encrypted_content


def decrypt_file(encrypted_content, key):
    """Decrypt encrypted content using the provided key."""
    try:
        cipher = Fernet(key)
        decrypted_content = cipher.decrypt(encrypted_content)
        return decrypted_content
    except Exception as e:
        return None
