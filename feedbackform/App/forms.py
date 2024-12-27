from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        exclude = ['created_at']
        widgets = {
            'username': forms.HiddenInput(),
            'phone_number': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        rating_fields = [
            'deity_rating', 'tilak_rating', 'leela_rating', 'samatha_rating',
            'deposit_rating', 'water_rating', 'wash_rating', 'accessibility_rating',
            'parking_rating', 'food_rating', 'shopping_rating', 'kids_rating',
            'entry_rating', 'directions_rating', 'overall_rating'
        ]
        
        for field in rating_fields:
            rating = cleaned_data.get(field)
            comment_field = f"{field.replace('_rating', '_comment')}"
            
            if rating and rating <= 2 and not cleaned_data.get(comment_field):
                raise forms.ValidationError(
                    f"Please provide feedback for the low rating of {field.replace('_rating', '').title()}"
                )
        
        return cleaned_data