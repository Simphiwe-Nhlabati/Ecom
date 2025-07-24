from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Shipping_Address, Order_View, Order_details
from .forms import CheckoutForm
from django.db import transaction
from django.urls import reverse_lazy
from django.conf import settings 
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils import timezone
from django.template.loader import render_to_string
from cart.models import Info_Product_Cart


# Create your views here.
@login_required
def check_out(request):
    
    cart_items = Info_Product_Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "There are no items in your cart.")
        return redirect(reverse_lazy('home_view'))

    try:
        info_address = Shipping_Address.objects.filter(user=request.user.user_profile).first()
        shipping_data = None
        if info_address:
            shipping_data = {
                'address': info_address.address,
                'city': info_address.city,
                'country': info_address.country,
            }
    except Exception as e:
        messages.warning(request, f"Error retrieving shipping address: {e}")
        shipping_data = {}

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    total = sum(item.product.price * item.quantity for item in cart_items)
                    
                    order = Order_View.objects.create(
                        user=request.user.user_profile,
                        total_price=total,
                        complete=True,
                        date=timezone.now()
                    )

                    for item in cart_items:
                        Order_details.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.price
                        )

                    cart_items.delete()

                    try:
                        current_site = get_current_site(request)
                        mail_subject = f"Order Confirmation - {current_site.domain}"
                        recipient_email = request.user.email
                        from_email = settings.DEFAULT_FROM_EMAIL

                        message_html = render_to_string('confirmation_order.html', {
                            'user': request.user,
                            'order': order,
                            'shipping_address': shipping_data,
                            'time_ordered': timezone.now(),
                        })

                        email = EmailMessage(
                            mail_subject,
                            message_html,
                            from_email,
                            [recipient_email]
                        )
                        email.content_subtype = 'html'
                        email.send()

                        messages.success(request, "Your order was placed successfully! A confirmation email has been sent.")
                        return redirect('home_dash')

                    except Exception:
                        messages.warning(request, f"Order placed has been successfully placed but could not send to email")
                        return redirect('home_dash')

            except Exception as e:
                messages.warning(request, f"Checkout failed: {e}")
        else:
            messages.warning(request, "Invalid form input.")
    else:
        form = CheckoutForm()

    return render(request, 'checkout/confirmation_order.html', {
        'form': form,
        'cart_items': cart_items,
        'total': sum(item.final_price() for item in cart_items),
        'shipping_address': shipping_data
    })
                
