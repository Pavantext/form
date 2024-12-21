from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.feedback_form, name='feedback_form'),
]