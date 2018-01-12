from celery import shared_task
from api_wrappers import twitter
from db.manager import save_tweets
import settings

client = twitter.APIWrapper(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)

@shared_task
def save_tweets():
    save_tweets(client.tweets_from_trends())
