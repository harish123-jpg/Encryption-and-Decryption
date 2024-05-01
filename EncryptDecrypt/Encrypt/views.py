import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
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


# Encrypt file using provided key
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(encrypted_data)


def home(request):
    if request.method == 'POST':
        if 'encryptFile' in request.FILES:
            uploaded_file = request.FILES['encryptFile']
            # Save the uploaded file temporarily
            with open('temp_file', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Generate or retrieve the key
            key = get_or_generate_key()
            # Encrypt the file
            encrypt_file('temp_file', key)
            # Optionally, you may delete the temporary file
            # os.remove('temp_file')
            # Serve the encrypted file for download
            encrypted_file_path = 'temp_file.encrypted'
            with open(encrypted_file_path, 'rb') as encrypted_file:
                response = HttpResponse(encrypted_file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(encrypted_file_path)
            return response
        else:
            return JsonResponse({'error': 'No file found'}, status=400)
    return render(request, 'home.html')


# Decrypt file using provided key
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_path.replace('.encrypted', ''), 'wb') as file:
        file.write(decrypted_data)


def decrypt_view(request):
    if request.method == 'POST':
        if 'decryptFile' in request.FILES:
            uploaded_file = request.FILES['decryptFile']
            # Save the uploaded file temporarily
            with open('temp_file.encrypted', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Retrieve the key
            key = get_or_generate_key()
            # Decrypt the file
            decrypt_file('temp_file.encrypted', key)
            # Serve the decrypted file for download
            decrypted_file_path = 'temp_file'
            with open(decrypted_file_path, 'rb') as decrypted_file:
                response = HttpResponse(decrypted_file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(decrypted_file_path)
            return response
        else:
            return JsonResponse({'error': 'No file found'}, status=400)
    return redirect('home')
