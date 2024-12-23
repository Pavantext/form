from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'deity_rating', 'tilak_rating', 'leela_rating', 'samatha_rating', 'deposit_rating', 'wash_rating', 'water_rating', 'accessibility_rating', 'parking_rating', 'food_rating', 'shopping_rating', 'kids_rating', 'overall_rating', 'feedback', 'contact', 'created_at']
    list_filter = ['created_at']
    search_fields = ['feedback', 'contact']
