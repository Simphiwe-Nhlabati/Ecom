from django.shortcuts import render
# from cart.models import Info_Product_Cart
from checkout.models import Order_View


# Create your views here.
def home_dash(request):
    # products = Info_Product_Cart.objects.all()
    recent_orders = Order_View.objects.filter(user=request.user.user_profile).order_by('date')[:10]
    return render(request, 'buyers/home_dashboard.html', 
                  {'recent_orders': recent_orders})