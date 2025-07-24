from django import forms
from .models import Product_in_Cart, Info_Product_Cart


class CartForm(forms.ModelForm):
    class Meta:
        model = Product_in_Cart
        fields = ('quantity',)


class UpdateCartForm(forms.ModelForm):
    class Meta:
        model = Info_Product_Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }


class RemoveCartItemForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())