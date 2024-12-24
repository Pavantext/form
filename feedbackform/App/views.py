from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from django.core.exceptions import PermissionDenied

# Create your views here.

def feedback_form(request):
    
    if request.method == 'POST':
       
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            # Set a session variable to indicate successful submission
            request.session['form_submitted'] = True
            return redirect('thank_you')
        else:
            messages.error(request, '❌ Please fill in all required ratings before submitting.')
    else:
        form = FeedbackForm()
    return render(request, 'feedbackform.html', {'form': form})

def thank_you(request):
    # Check if the form was actually submitted
    if not request.session.get('form_submitted', False):
        raise PermissionDenied
    
    # Clear the session variable
    request.session['form_submitted'] = False
    return render(request, 'thankyou.html')
