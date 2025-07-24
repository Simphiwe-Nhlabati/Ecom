from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name="ProductView"),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
]