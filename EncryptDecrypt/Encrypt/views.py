from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from cryptography.fernet import Fernet
import os

from .utils import get_or_generate_key, encrypt_file

def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(data)
        file_content = decrypted_data.split(b'--SPLIT--', 1)
        file_password = file_content[0].decode()
        # Return the decrypted password and data
        return file_password, file_content[1]
    except Exception as e:
        return None, None


# Define the decrypt_file view
def decrypt_file_view(request):
    if request.method == 'POST':
        # Check if the file and password are provided
        if 'decryptFile' in request.FILES:
            uploaded_file = request.FILES['decryptFile']
            provided_password = request.POST.get('password')
            # Save the uploaded file to disk
            with open('temp_file.encrypted', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Retrieve the encryption key
            key = cache.get('encryption_key')
            # Decrypt the file and get the password and data
            decrypted_password, decrypted_data = decrypt_file('temp_file.encrypted', key)
            if decrypted_password == provided_password:
                # Save the decrypted data to a new file
                with open('temp_file.decrypted', 'wb') as file:
                    file.write(decrypted_data)
                decrypted_file_path = 'temp_file.decrypted'
                with open(decrypted_file_path, 'rb') as decrypted_file:
                    response = HttpResponse(decrypted_file.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(decrypted_file_path)
                return response
            else:
                return JsonResponse({'error': 'Incorrect password or file not found'}, status=400)
        else:
            return JsonResponse({'error': 'No file found'}, status=400)
    return redirect('home')


# View function for handling file upload and download
def home(request):
    if request.method == 'POST':
        if 'encryptFile' in request.FILES:
            uploaded_file = request.FILES['encryptFile']
            password = request.POST.get('password')
            with open('temp_file', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Retrieve or generate the encryption key
            key = get_or_generate_key()
            # Encrypt the file
            encrypt_file('temp_file', key, password)
            encrypted_file_path = 'temp_file.encrypted'
            with open(encrypted_file_path, 'rb') as encrypted_file:
                response = HttpResponse(encrypted_file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(encrypted_file_path)
            return response
        else:
            return JsonResponse({'error': 'No file found'}, status=400)
    return render(request, 'home.html')
