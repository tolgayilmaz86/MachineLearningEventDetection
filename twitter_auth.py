from tweepy import OAuthHandler

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

_auth = None

def authenticate():
  global _auth 
  if _auth:
      return _auth
  _auth = OAuthHandler(consumer_key, consumer_secret)
  _auth.set_access_token(access_token, access_token_secret)
  return _auth
