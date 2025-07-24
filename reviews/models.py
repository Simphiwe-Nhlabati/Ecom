from django.db import models
from django.conf import settings
from vendors.models import Product


# Create your models here.
class Review_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(1, '1 star'), 
                                          (2, '2 stars'), 
                                          (3, '3 stars'), 
                                          (4, '4 stars'), 
                                          (5, '5 stars')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Review made by {self.user} for a product named {self.product.name}"