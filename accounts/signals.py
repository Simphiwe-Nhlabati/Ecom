# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import User_Profile


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         User_Profile.objects.get(
#             user=instance,
#             email=instance.email,
#             first_name=instance.first_name,
#             last_name=instance.last_name,
#             user_type='buyer'  # default role; change as needed
#         )
        
        