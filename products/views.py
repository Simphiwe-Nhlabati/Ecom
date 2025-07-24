from django.shortcuts import render, get_object_or_404
from .models import ProductView
from vendors.models import Product
from reviews.models import Review_product


# Create your views here.
def home_view(request):
    products = ProductView.objects.all()
    return render(request, 'accounts/home.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review_product.objects.filter(product=product)
    return render(request, 'cart/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })