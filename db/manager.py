from db import models

id = 0
class SessionManager:

    def __init__(self, sm=models.SESSIONMAKER):
        self.sessiomaker = sm

    def __enter__(self):
        self.session = self.sessionmaker()
        return self.session

    def __exit__(self, *args):
        self.session.close()


def save_tweets(tweets):
    with SessionManager() as sm:
        db_tweets = []
        for tweet in tweets:
            db_tweets.append(models.Tweet(id=id,
                                         username=tweet['username'],
                                         created_at=tweet['created_at'],
                                         text=tweet['text'],
                                         ))
            id += 1
        sm.add_all(db_tweets)
        sm.commit()
