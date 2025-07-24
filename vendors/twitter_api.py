import tweepy
from django.conf import settings


def obtain_twitter_api():
    """
    Obtain a Twitter API client using the credentials from settings.
    """
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET_KEY,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    
    api = tweepy.API(auth)
    
    try:
        api.verify_credentials()
        print("Twitter API credentials are valid.")
    except Exception as e:
        print(f"Error verifying Twitter API credentials: {e}")
    
    return api