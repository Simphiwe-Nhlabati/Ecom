from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Store, Product
from .serializers import StoreSerializer, ProductSerializer
from .form import EStoreForm, EProductForm
from checkout.models import Order_details
from accounts.models import User_Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, F
from django.utils.text import slugify
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from accounts.permissions import VendorPem, BuyerPem
# Create your views here.


class Store_View(LoginRequiredMixin, ListView):
    """View all stores for the vendor."""
    model = Store
    permission_classes = [IsAuthenticated, VendorPem, BuyerPem]
    serializer_class = StoreSerializer
    template_name = 'vendors/store_view.html'
    context_object_name = 'stores'

    def obtain_store(self):
        return self.request.user.stores.all()
    

class Store_Generate(LoginRequiredMixin, CreateView):
    """Create a new store for the vendor."""
    model = Store
    form_class = EStoreForm
    permission_classes = [IsAuthenticated, VendorPem]
    serializer_class = StoreSerializer
    template_name = 'vendors/store_form.html'
    success_url = reverse_lazy('vendors:store_view')

    def form_valid(self, form):
        form.instance.vendor = self.request.user.user_profile
        web_slug = slugify(form.instance.name)
        slug = web_slug
        number = 1
        while Store.objects.filter(slug=slug).exists():
            slug = f"{web_slug}-{number}"
            number += 1
        form.instance.slug = slug
        return super().form_valid(form)
    
    
class Store_Generate_API(CreateAPIView):
    """API endpoint to create a new store for the vendor."""
    form_class = EStoreForm
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticated, VendorPem]
    serializer_class = StoreSerializer
    # template_name = 'vendors/store_form.html'
    success_url = reverse_lazy('vendors:store_view')
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.user_profile)


class Store_Update(LoginRequiredMixin, UpdateView):
    """Update an existing store for the vendor."""
    model = Store
    form_class = EStoreForm
    permission_classes = [IsAuthenticated, VendorPem]
    # fields = ['name', 'description']
    template_name = 'vendors/store_form.html'
    success_url = reverse_lazy('vendors:store_view')

    def get_queryset(self):
        return Store.objects.filter(vendor=self.request.user.user_profile)


class Store_delete(LoginRequiredMixin, DeleteView):
    """Delete a store from the vendor's list."""
    model = Store
    # form_class = EStoreForm
    permission_classes = [IsAuthenticated, VendorPem]
    template_name = 'vendors/store_delete.html'
    success_url = reverse_lazy('vendors:store_view')

    def get_queryset(self):
        return Store.objects.filter(vendor=self.request.user.user_profile)
    

@login_required
def home_vendor(request):
    """Render the home dashboard for the vendor."""
    dash_list = {
        'stores': Store.objects.filter(vendor=request.user.user_profile),
        'products': Product.objects.filter(store__vendor=request.user.user_profile)
    }
    return render(request, 'vendors/home_dashboard.html', {'dash_list': dash_list})

    
@login_required
def view_product(request, store_id):
    """View all products in the store."""
    store = get_object_or_404(Store, pk=store_id, vendor=request.user.user_profile)

    products = Product.objects.filter(store=store)
    return render(request, 'vendors/view_product.html', {'store': store, 'products': products})


@login_required
# @api_view(['POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated, VendorPem])
def generate_product(request):
    if not Store.objects.filter(vendor__user=request.user).exists():
        messages.error(request, "You don't have any stores. Please create one first.")
        return redirect('vendors:store_generate')

    if request.method == 'POST':
        form = EProductForm(request.POST, user=request.user)
        # serializer = ProductSerializer(data=request.data)
        if form.is_valid():
            product = form.save(commit=False)
            selected_store = form.cleaned_data.get('store')

        else:
            messages.error(request, "Please correct the errors below.")

        if selected_store:
            product.store = selected_store
            product.save()
            messages.success(request, f"Product '{product.name}' added successfully.")
            return redirect('vendors:view_product', store_id=selected_store.id)
        else:
            messages.error(request, "Please select a valid store.")
    
    else:
        form = EProductForm(user=request.user)  # ✅ Pass the user
        # serializer = ProductSerializer()

    return render(request, 'vendors/product_form.html', {
        'form': form
    })
    # return render(request, 'vendors/product_form.html', {
    #     'form': serializer 
    # })
    

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def generate_product_api(request):
    # Ensure the vendor has a store
    
    # if not Store.objects.filter(vendor__user=request.user).exists():
    #     return Response(
    #         {"detail": "You don't have any stores. Please create one first."},
    #         status=HTTP_403_FORBIDDEN
    #     )
    
    try:
        store = Store.objects.get(vendor__user=request.user)
    except Store.DoesNotExist:
        return Response(
            {"detail": "You don't have any stores. Please create one first."},
            status=HTTP_403_FORBIDDEN
        )

    serializer = ProductSerializer(data=request.data, context={'store': store})
    if serializer.is_valid():
        product = serializer.save()
        return Response({
            "message": f"Product '{product.name}' added successfully.",
            "product_id": product.id,
            "store_id": product.store.id
        })
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@login_required
def modify_product(request, pk):
    """Modify an existing product in the store."""
    product_to_modify = get_object_or_404(Product, pk=pk, store__vendor=request.user.user_profile)
    store = None
    try:
        store = Product.objects.first() 
    except Product.DoesNotExist:
        pass
    
    user = request.user

    # if not user.has_perm('modify_product'):
    #     form = EProductForm(instance=product_to_modify) 
    #     return render(request, 'vendors/product_form.html', {'form': form, 'store': store, 'error_message': "You don't have permission to change products."})

    if request.method == 'POST':
        form = EProductForm(request.POST, instance=product_to_modify)
        if 'store' in form.fields:
            del form.fields['store']
            
        # else:
        #     form = EProductForm(instance=product_to_modify)
        #     if 'store' in form.fields:
        #         del form.fields['store']
        
        if form.is_valid():
            product_instance = form.save(commit=False) 
            product_instance.save()
            messages.success(request, f"Product '{product_instance.name}' has been modify.")
            url = reverse_lazy('vendors:view_product', args=[product_instance.store.id])
            return HttpResponseRedirect(url)
        else:
            messages.error(request, "The modification of the product was unsuccessful")
            return render(request, 'vendors/product_form.html', {'form': form, 'store': store})
    
    else: 
        form = EProductForm(instance=product_to_modify)
        if 'store' in form.fields:
            del form.fields['store'] 
    
    return render(request, 'vendors/product_form.html', {'form': form, 'store': store})
    
    
@login_required
def delete_product(request, pk):
    """Delete a product from the store."""
    product_to_delete = get_object_or_404(Product, pk=pk, store__vendor=request.user.user_profile)
    # user = request.user

    store_context = None 

    if request.method == 'POST':

        try:
            store_id = product_to_delete.store.id
            product_to_delete.delete()
            messages.success(request, f"Product '{product_to_delete.name}' deleted successfully.")
            url = reverse_lazy('vendors:view_product', args=[store_id])
            return HttpResponseRedirect(url)
        except Exception as e: 
            messages.error(request, f"An error occurred while deleting the product: {e}")
            return render(request, 'vendors/delete_product.html', {'product': product_to_delete, 'store': store_context}) 
        
    else:
        return render(request, 'vendors/delete_product.html', {'product': product_to_delete, 'store': store_context})


@login_required
def sales_report(request):
    try:
        user_profile = User_Profile.objects.get(user=request.user)  
    except User_Profile.DoesNotExist:
        messages.error(request, "No user profile found.")
        return render(request, 'vendors/sales_report.html', {
            'report': [],
            'stores': [],
            'selected_store': None
        })

    store_id = request.GET.get('store')

    if store_id:
        try:
            selected_store = Store.objects.get(id=store_id, vendor=user_profile)
            orders = Order_details.objects.filter(product__store=selected_store)
        except Store.DoesNotExist:
            messages.error(request, "Invalid store selected.")
            orders = Order_details.objects.none()
            selected_store = None
    else:
        orders = Order_details.objects.filter(product__store__vendor=user_profile)
        selected_store = None

    report = (
        orders
        .values('product__id', 'product__name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('price') * F('quantity'))
        )
        .order_by('total_revenue')
    )

    stores = Store.objects.filter(vendor=user_profile)

    return render(request, 'vendors/sales_report.html', {
        'report': report,
        'stores': stores,
        'selected_store': int(store_id) if store_id else None
    })
    

def api_handler(request):
    """Handle AI-related requests."""
    if request.method == 'POST':
        # Process the AI request here
        # For example, you can use OpenAI's API to generate a response
        pass
    else:
        # Render a form or page for AI interaction
        return render(request, 'vendors/ai_handler.html')
    
