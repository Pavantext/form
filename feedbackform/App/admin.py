from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'deity_rating', 'tilak_rating', 'leela_rating', 'samatha_rating', 'deposit_rating', 'water_rating',  'overall_rating', 'created_at']
    list_filter = ['created_at']
    search_fields = ['feedback', 'contact']
