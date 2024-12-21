from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm

# Create your views here.

def feedback_form(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback_form')
    else:
        form = FeedbackForm()
    return render(request, 'feedbackform.html', {'form': form})
