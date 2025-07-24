from rest_framework import permissions
from .models import User_Profile


class BuyerPem(permissions.BasePermission):
    """
    Custom permission to only allow buyers to access certain views.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        profile, created = User_Profile.objects.get_or_create(
            user=request.user,
            defaults={
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'user_type': 'buyer',
            }
        )
        return profile.user_type == 'buyer'
    

class VendorPem(permissions.BasePermission):
    """
    Custom permission to only allow vendors to access certain views.
    """

    # def has_permission(self, request, view):
    #     if not request.user or not request.user.is_authenticated:
    #         return False
        
    #     try:
    #         profile, _ = User_Profile.objects.get_or_create(
    #             user=request.user,
    #             defaults={
    #                 'email': request.user.email,
    #                 'first_name': request.user.first_name,
    #                 'last_name': request.user.last_name,
    #                 'user_type': 'buyer',
    #             }
    #         )
    #         return profile.user_type == 'vendor'
        
    #     except Exception as e:
    #         print(["Error in VendorPem permission:", str(e)])
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = User_Profile.objects.get(user=request.user)
            return profile.user_type == 'vendor'
        except User_Profile.DoesNotExist:
            return False
            