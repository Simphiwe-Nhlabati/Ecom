from django.db import models
from vendors.models import Product
from accounts.models import User_Profile


# Create your models here.
class Order_View(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Order is made by {self.user} and total price is {self.total_price}"
    
    
class Order_details(models.Model):
    """
    Represents a single product within an order.
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order_View, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The product name is {self.product} with the quantity of {self.quantity} and final price of {self.price}"
    
    def final_prices(self):
        return self.quantity * self.price
    
    
class Shipping_Address(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.OneToOneField(Order_View, on_delete=models.CASCADE, null=True, blank=True, related_name='shipping_address')
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False, default='South Africa')
    date_made = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The name of the user {self.user}, the address {self.address} and the date {self.date_made}"