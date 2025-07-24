from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name="home_view"),
    # path("login/", views.login_vendor, name="login_vendor"),
    # path("logout/", views.logout_vendor, name="logout_vendor"),
    # path("login/", views.login_buyer, name="login_buyer"),
    # path("logout/", views.logout_buyer, name="logout_buyer"),
    # path("register/", views.register_buyer, name="register_buyer"),
    path("register/", views.register_user, name="register_user"),
    # path("reset/", views.rest_password_buyer, name="reset_password_buyer"),
    # path("reset/", views.reset_vendor_password, name="reset_vendor_password"),
    # path("reset/", views.reset_buyer_password, name="reset_buyer_password"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("reset_password/", views.reset_user_password, name="reset_password"),
    path('password_confirmation/<int:user_id>/<str:token>/', views.password_confirmation, name='password_confirmation'),
]
