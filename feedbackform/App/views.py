from django.shortcuts import render

# Create your views here.

def feedbackform(request):
    return render(request, 'feedbackform.html')
