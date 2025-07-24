from django import forms
from .models import Store, Product


class EStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description',]       
        

class EProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'stock', 'store']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        
        if user is not None:
            self.fields['store'].queryset = Store.objects.filter(vendor__user=user) 
        else:
            self.fields['store'].queryset = Store.objects.none()