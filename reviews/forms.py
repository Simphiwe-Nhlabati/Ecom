from django import forms
from .models import Review_product


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review_product
        fields = ('text', 'rating')