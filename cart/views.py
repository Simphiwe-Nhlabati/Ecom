from django.shortcuts import render, get_object_or_404
# from products.models import ProductView
from vendors.models import Product
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UpdateCartForm, CartForm
from .models import Info_Product_Cart, Product_in_Cart


# Create your views here.
def add_item_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            
            quantity = form.cleaned_data.get('quantity', 1)

            product_cart, _ = Product_in_Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'product_amount': product.price * quantity}
            )

            cart_item, created = Info_Product_Cart.objects.get_or_create(
                cart=product_cart,
                product=product,
                defaults={
                    'user': request.user,
                    'price': product.price,
                    'quantity': quantity,
                    'specification': "",
                }
            )
            
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f"{product.name} added to your cart.")
            return redirect('show_user_cart')
        else:
            messages.error(request, "Failed to add item to cart.")
    return render(request, 'cart/add_to_cart.html', {'form': form, 'product': product})


def update_cart_item(request, item_id):
    item = get_object_or_404(Info_Product_Cart, id=item_id, user=request.user)
    form = UpdateCartForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"{item.product.name} updated.")
        return redirect('show_user_cart')
    return render(request, 'cart/update_cart.html', {'form': form, 'item': item})


def remove_cart_item(request, item_id):
    item = get_object_or_404(Info_Product_Cart, id=item_id, user=request.user)
    item.delete()
    messages.success(request, f"{item.product.name} removed from cart.")
    return redirect('show_user_cart')
      

def show_user_cart(request):
    cart_items = Info_Product_Cart.objects.filter(user=request.user)
    total = sum(item.final_price() for item in cart_items)
    return render(request, 'cart/main_cart.html', {'cart_items': cart_items, 'total': total})