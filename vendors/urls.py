from django.urls import path
from . import views

app_name = 'vendors' 

urlpatterns = [
    path('home_vendor/', views.home_vendor, name="home_vendor"),
    path('store_View/', views.Store_View.as_view(), name="store_view"),
    path('generate_store/', views.Store_Generate.as_view(), name="store_generate"),
    path('api/generate_store_api/', views.Store_Generate_API.as_view(), name="store_generate_api"),
    path('store_Update/<int:pk>/', views.Store_Update.as_view(), name="store_update"),
    path('store_delete/<int:pk>/', views.Store_delete.as_view(), name="store_delete"),
    path('view_product/<int:store_id>/', views.view_product, name="view_product"),
    path('generate_product/', views.generate_product, name="generate_product"),
    path('api/generate_product_api/', views.generate_product_api, name="generate_product_api"),
    path('modify_product/<int:pk>/modify/', views.modify_product, name="modify_product"),
    path('delete_product/<int:pk>/delete/', views.delete_product, name="delete_product"),
    path('sales_report/', views.sales_report, name='sales_report'),
]