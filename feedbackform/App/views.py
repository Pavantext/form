from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .utils import encrypt_data, decrypt_data
from django.http import JsonResponse
from .notifications import send_notifications
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def feedback_form(request):
    if request.method == 'GET':
        try:
            # Check if we have encrypted data
            encrypted_data = request.GET.get('data', '')
            if encrypted_data:
                # Decrypt the data
                data = decrypt_data(encrypted_data)
                if not data:
                    logger.error(f"Failed to decrypt data: {encrypted_data[:30]}...")
                    messages.error(request, "Invalid or expired link. Please try again.")
                    return redirect('home')
                
                username = data.get('username', '')
                phone_number = data.get('phone', '')
                email = data.get('email', '')
                location = data.get('location', '')
                
                logger.info(f"Successfully decrypted data for user: {username}")
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

        except Exception as e:
            logger.error(f"Error processing feedback form: {str(e)}")
            messages.error(request, "An error occurred. Please try again.")
            return redirect('home')
    
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

@csrf_exempt
def send_bulk_notifications(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            subject = data.get('subject', 'Notification')
            
            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)
                
            results = send_notifications(message, subject)
            return JsonResponse({
                'status': 'success',
                'results': results
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def test_notification(request):
    """Test endpoint to send a single notification"""
    try:
        if request.method in ['GET', 'POST']:
            # For GET request, use default values or query parameters
            if request.method == 'GET':
                name = request.GET.get('name', '')
                username = request.GET.get('username', '')
                phone = request.GET.get('phone', '')
                email = request.GET.get('email', '')
                location = request.GET.get('location', '')
            else:  # POST request
                data = json.loads(request.body)
                name = data.get('name', '')
                username = data.get('username', '')
                phone = data.get('phone', '')
                email = data.get('email', '')
                location = data.get('location', '')

            context = {
                'name': name,
                'username': username,
                'phone': phone,
                'email': email,
                'location': location
            }

            subject = "State of Equality Feedback"
            message = f"Thank you {name} for visiting State of Equality"  # Base message
            results = send_notifications(message, subject, context)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Test notification sent',
                'results': results
            })
        return JsonResponse({'error': 'Only GET and POST requests are allowed'}, status=405)
    except Exception as e:
        logger.error(f"Error in test_notification: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
