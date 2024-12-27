from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone_number', 'deity_rating', 'deity_comment', 'tilak_rating', 'tilak_comment', 'leela_rating', 'leela_comment', 'samatha_rating', 'samatha_comment', 'deposit_rating', 'deposit_comment', 'wash_rating', 'wash_comment', 'water_rating', 'water_comment', 'accessibility_rating', 'accessibility_comment', 'parking_rating', 'parking_comment', 'food_rating', 'food_comment', 'shopping_rating', 'shopping_comment', 'kids_rating', 'kids_comment', 'entry_rating', 'entry_comment', 'directions_rating', 'directions_comment', 'overall_rating', 'overall_comment', 'feedback', 'contact', 'created_at']
    list_filter = ['created_at']
    search_fields = ['feedback', 'contact']
