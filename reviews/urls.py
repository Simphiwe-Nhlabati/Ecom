from django.urls import path
from . import views 

urlpatterns = [
    path('product_review/<int:product_id>/', views.make_review, name="make_review"),
    path('api/list_review/', views.display_reviews_api, name="display_reviews_api"),
]