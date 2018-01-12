import requests
import base64
import json



class APIWrapper:
    def __init__(self, consumer_key, consumer_secret):
        self.base_url = 'https://api.twitter.com/'
        self.token = None
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth()


    @property
    def _base64_key_secret(self):
        key_secret = "{}:{}".format(self.consumer_key, self.consumer_secret).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')
        return b64_encoded_key

    def auth(self):
        auth_url = '{}oauth2/token'.format(self.base_url)
        auth_headers = {
            'Authorization': 'Basic {}'.format(self._base64_key_secret),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        auth_data = {
            'grant_type': 'client_credentials'
        }
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
        self.token = json.loads(auth_resp.content.decode()).get('access_token', None)

    def _check_auth(func):
        def wrapper(self, *args, **kwargs):
            if self.token is None:
                self.auth()
            return func(self, *args, **kwargs)
        return wrapper

    @_check_auth
    def get_trends(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        url = '{}1.1/trends/place.json?id=1'.format(self.base_url)
        resp = requests.get(url, headers=headers)
        data = json.loads(resp.content.decode())
        trends = next(iter(data), {}).get("trends", "No trends")
        return trends

    @_check_auth
    def search_tweets(self, q, count=5):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        search_params = {
            'q': q,
            'result_type': 'recent',
            'count': count
        }

        url = '{}1.1/search/tweets.json'.format(self.base_url)
        resp = requests.get(url, headers=headers, params=search_params)
        whole_tweets = json.loads(resp.content.decode()).get('statuses')
        tweets = []
        for t in whole_tweets:
            tweet = {}
            tweet["text"] = t.get("text", None)
            tweet["username"] = t.get("user", {}).get("name", None)
            tweet["created_at"] = t.get("created_at", "")
            tweet["hashtags"] = t.get("entities", {}).get("hashtags", None)
            tweets.append(tweet)
        return tweets

    @_check_auth
    def tweets_from_trends(self, trends_count=10, count=5):
        tweets = []
        for index, trend in enumerate(self.get_trends()):
            if index >= trends_count:
                break
            tweets += self.search_tweets(trend.get('name'), count)
        return tweets


if __name__ == "__main__":
    client = APIWrapper()
    print(client.tweets_from_trends())
    # trends = get_trends()
    # print(trends)