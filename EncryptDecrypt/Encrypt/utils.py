from cryptography.fernet import Fernet
from django.core.cache import cache


# Generate a key
def generate_key():
    return Fernet.generate_key()


def get_or_generate_key():
    key = cache.get('encryption_key')
    if not key:
        key = generate_key()
        cache.set('encryption_key', key, timeout=None)  # Set timeout=None for indefinite caching
    return key


# Encrypt file using provided key and password
def encrypt_file(file_path, key, password):
    with open(file_path, 'rb') as file:
        data = file.read()
    cipher_suite = Fernet(key)
    # Include the password in the encrypted data
    encrypted_data = cipher_suite.encrypt(password.encode() + b'--SPLIT--' + data)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(encrypted_data)
