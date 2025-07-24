from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review_product
from .forms import ReviewForm
from django.contrib import messages
from vendors.models import Product
from checkout.models import Order_details
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from vendors.serializers import ReviewSerializer


# Create your views here.
@login_required
# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def make_review(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)

    has_purchased = Order_details.objects.filter(
        order__user=request.user.user_profile,
        product=product
    ).exists()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.is_verified = has_purchased
            review.save()
            messages.success(request, 'Your review was submitted successfully.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_product.html', {
        'form': form,
        'product': product,
        'is_verified': has_purchased
    })
    

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def display_reviews_api(request):
    user_profile = request.user.user_profile
    reviews = Review_product.objects.filter(product__store__vendor=user_profile)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
