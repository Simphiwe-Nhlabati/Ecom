from django.urls import path
from . import views

urlpatterns = [
    # path('retreive_products/', views.retreive_products, name="retreive_products"),
    path('add_item/<int:product_id>/', views.add_item_to_cart, name="add_item_to_cart"),
    path('update_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('show_cart/', views.show_user_cart, name="show_user_cart"),
]