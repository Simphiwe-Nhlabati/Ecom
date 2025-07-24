from django.urls import path
from . import views

urlpatterns = [
    path('home_dash/', views.home_dash, name="home_dash"),
]