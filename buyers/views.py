from django.shortcuts import render
from cart.models import Info_Product_Cart


# Create your views here.
def home_dash(request):
    products = Info_Product_Cart.objects.all()
    return render(request, 'buyers/home_dashboard.html', {'products': products})