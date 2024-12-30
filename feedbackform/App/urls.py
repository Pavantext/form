from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('thank_you/', views.thank_you, name='thank_you'),
]