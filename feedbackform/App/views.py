from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from django.core.exceptions import PermissionDenied

# Create your views here.

def feedback_form(request):
    # Get parameters from URL
    username = request.GET.get('username', '')
    phone_number = request.GET.get('phone', '')
    
    if request.method == 'POST':
        # Include the URL parameters in the form data
        form_data = request.POST.copy()
        form_data['username'] = username
        form_data['phone_number'] = phone_number
        
        form = FeedbackForm(form_data)
        if form.is_valid():
            form.save()
            request.session['form_submitted'] = True
            return redirect('thank_you')
        else:
            messages.error(request, '❌ Please fill in all required ratings before submitting.')
    else:
        # Initialize form with URL parameters
        form = FeedbackForm(initial={
            'username': username,
            'phone_number': phone_number
        })
    
    return render(request, 'feedbackform.html', {
        'form': form,
        'username': username,
        'phone_number': phone_number
    })

def thank_you(request):
    # Check if the form was actually submitted
    if not request.session.get('form_submitted', False):
        raise PermissionDenied
    
    # Clear the session variable
    request.session['form_submitted'] = False
    return render(request, 'thankyou.html')
