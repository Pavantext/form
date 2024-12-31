from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse
import base64
import json
from cryptography.fernet import Fernet
from django.conf import settings

# Create encryption key and Fernet instance
# Add this to your Django settings.py:
# ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data):
    json_data = json.dumps(data)
    encrypted_data = fernet.encrypt(json_data.encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()

def decrypt_data(encrypted_data):
    try:
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = fernet.decrypt(decoded_data)
        return json.loads(decrypted_data.decode())
    except:
        return None

def home(request):
    return render(request, 'home.html')

def feedback_form(request):
    if request.method == 'GET':
        # Check if we have encrypted data
        encrypted_data = request.GET.get('data', '')
        if encrypted_data:
            # Decrypt the data
            data = decrypt_data(encrypted_data)
            if not data:
                return redirect('home')
            username = data.get('username', '')
            phone_number = data.get('phone', '')
            email = data.get('email', '')
            location = data.get('location', '')
        else:
            # Get raw parameters (for first submission from home page)
            username = request.GET.get('username', '')
            phone_number = request.GET.get('phone', '')
            email = request.GET.get('email', '')
            location = request.GET.get('location', '')
            
            # Encrypt and redirect if we have data
            if username and phone_number:
                data = {
                    'username': username,
                    'phone': phone_number,
                    'email': email,
                    'location': location
                }
                encrypted_data = encrypt_data(data)
                return redirect(f"{reverse('feedback_form')}?data={encrypted_data}")
    
    elif request.method == 'POST':
        # Handle form submission
        encrypted_data = request.GET.get('data', '')
        data = decrypt_data(encrypted_data) if encrypted_data else {}
        
        form_data = request.POST.copy()
        form_data['username'] = data.get('username', '')
        form_data['phone_number'] = data.get('phone', '')
        form_data['email'] = data.get('email', '')
        form_data['location'] = data.get('location', '')
        
        form = FeedbackForm(form_data)
        if form.is_valid():
            form.save()
            request.session['form_submitted'] = True
            return redirect('thank_you')
        else:
            messages.error(request, '❌ Please fill in all required ratings before submitting.')
    
    # Initialize form
    form = FeedbackForm(initial={
        'username': username,
        'phone_number': phone_number,
        'email': email,
        'location': location
    })
    
    return render(request, 'feedbackform.html', {
        'form': form,
        'username': username,
        'phone_number': phone_number,
        'email': email,
        'location': location
    })

def thank_you(request):
    if not request.session.get('form_submitted', False):
        raise PermissionDenied
    request.session['form_submitted'] = False
    return render(request, 'thankyou.html')
