from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model

# User = get_user_model


# Create your models here.
class User_Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    def __str__(self):
        return f"User's username:{self.user} Email:{self.email}"
    
    
class ResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"user:{self.user} token:{self.token} "