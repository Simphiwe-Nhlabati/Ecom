from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from .models import User_Profile


@receiver(post_save, sender=User_Profile)
def assign_user_to_group(sender, instance, created, **kwargs):
    if not created:
        return

    user_type = instance.user_type.lower().capitalize()  
    group, _ = Group.objects.get_or_create(name=user_type)
    instance.groups.add(group)

    if user_type == 'Buyer':
        
        assign_permissions_to_group(group, ['view_product', 'store_view'])

    elif user_type == 'Vendor':
        
        assign_permissions_to_group(group, [
            'generate_product', 'modify_product', 'delete_product', 'view_product',
            'store_generate', 'store_update', 'store_delete', 'store_view', 'sales_report'
        ])


def assign_permissions_to_group(group, codename_list):
    """Assign a list of permission codenames to a group dynamically."""
    models = {
        'product': apps.get_model('vendors', 'Product'),
        'store': apps.get_model('vendors', 'Store'),
    }

    for codename in codename_list:
        model_key = codename.split('_')[-1]
        model_key = model_key.lower()
        
        if model_key not in models:
            continue

        try:
            permission = Permission.objects.get(
                codename=codename,
                content_type__app_label='vendors',
                content_type__model=model_key
            )
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            pass