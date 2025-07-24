from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Store, Product
from .twitter_api import obtain_twitter_api


@receiver(post_save, sender=Store)
def tweet_new_store(sender, instance, created, **kwargs):
    if created:
        client = obtain_twitter_api()
        tweet_text = f"New store added!\n\n {instance.name}\n {instance.description}"
        client.update_status(status=tweet_text)
        

@receiver(post_save, sender=Product)        
def tweet_new_product(sender, instance, created, **kwargs):
    if created:
        client = obtain_twitter_api()
        store_name = instance.store.name
        tweet_text = f"New product added!\n\n {store_name}\n {instance.name}\n {instance.description}"
        client.update_status(status=tweet_text)