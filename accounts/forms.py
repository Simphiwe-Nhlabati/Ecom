from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User_Profile
from django.contrib.auth.models import User
from django import forms


class UserSignUpForm(UserCreationForm):
    
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',]
        
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = '<span class="form-text text-muted"><small>Required. Enter a valid email address.</small></span>'
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['first_name'].label = 'First Name'
        
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['last_name'].label = 'Last Name'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Required. 8 characters or more. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>The password should match each other.</small></span>'
        
        self.fields['user_type'].widget.attrs['class'] = 'form-control'
        self.fields['user_type'].widget.attrs['placeholder'] = 'Select your user_type'
        self.fields['user_type'].label = 'User_type'
        self.fields['user_type'].help_text = '<span class="form-text text-muted"><small>Select your option.</small></span>'
        

class UserRestPassword(PasswordResetForm):
    
    class Meta(PasswordResetForm):
        model = User_Profile
        fields = ('email',)
        

