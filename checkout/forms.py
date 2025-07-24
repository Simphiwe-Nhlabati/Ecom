from django import forms
from .models import Shipping_Address


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Shipping_Address
        fields = ['country', 'city']