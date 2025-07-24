from django.db import models
from django.conf import settings
from vendors.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Product_in_Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    product_amount = models.DecimalField(max_digits=7, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
        return f"quantity:{self.quantity}"
    
    def total_price(self):
        return self.quantity * self.product_amount
    

class Info_Product_Cart(models.Model):
    cart = models.ForeignKey(Product_in_Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.TextField(blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    
    def __str__(self):
        return f"name:{self.cart} specification:{self.specification}"
    
    def final_price(self):
        return self.quantity * self.price