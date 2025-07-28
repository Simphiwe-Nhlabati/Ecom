from django import forms
from .models import Store, Product


class EStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the name of the store'
        self.fields['name'].label = 'Name'
        self.fields['name'].help_text = '<span class="form-text text-muted"><small>Required. 100 characters or fewer.</small></span>'
        
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter the description of the store'
        self.fields['description'].label = 'Description'
        self.fields['description'].help_text = '<span class="form-text text-muted"><small>Required. 255 characters or fewer.</small></span>'       
        

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
            
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the name of the product'
        self.fields['name'].label = 'Name'
        self.fields['name'].help_text = '<span class="form-text text-muted"><small>Required. 100 characters or fewer.</small></span>'
        
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter the description of the product'
        self.fields['description'].label = 'Description'
        self.fields['description'].help_text = '<span class="form-text text-muted"><small>Optional. 255 characters or fewer.</small></span>'
        
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['placeholder'] = 'Enter the price of the product'
        self.fields['price'].label = 'Price'
        self.fields['price'].help_text = '<span class="form-text text-muted"><small>Required. Enter a valid price.</small></span>'
        
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['placeholder'] = 'Enter the image of the product'
        self.fields['image'].label = 'Image'
        self.fields['image'].help_text = '<span class="form-text text-muted"><small>Optional. Upload an image of the product.</small></span>'
        
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['placeholder'] = 'Enter the stock of the product'
        self.fields['stock'].label = 'Stock'
        self.fields['stock'].help_text = '<span class="form-text text-muted"><small>Required. Enter a valid stock.</small></span>'
        
        self.fields['store'].widget.attrs['class'] = 'form-control'
        self.fields['store'].widget.attrs['placeholder'] = 'Select the store of the product'
        self.fields['store'].label = 'Store'
        self.fields['store'].help_text = '<span class="form-text text-muted"><small>Required. Select the store of the product.</small></span>'
        