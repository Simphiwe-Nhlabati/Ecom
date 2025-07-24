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
        

class UserRestPassword(PasswordResetForm):
    
    class Meta(PasswordResetForm):
        model = User_Profile
        fields = ('email',)
        

