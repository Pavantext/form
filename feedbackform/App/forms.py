from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        exclude = ['created_at']

    def clean(self):
        cleaned_data = super().clean()
        # Check if all rating fields are filled
        rating_fields = [
            'deity_rating', 'tilak_rating', 'leela_rating', 'samatha_rating',
            'deposit_rating', 'water_rating', 'wash_rating', 'accessibility_rating',
            'parking_rating', 'food_rating', 'shopping_rating', 'kids_rating',
            'entry_rating', 'directions_rating', 'overall_rating'
        ]
        
        for field in rating_fields:
            if not cleaned_data.get(field):
                raise forms.ValidationError(f"Please provide a rating for {field.replace('_rating', '').title()}")
        
        return cleaned_data