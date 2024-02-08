from tweepy import OAuthHandler

access_token = "721070683476860928-TY8VxNshpLqRrZ7fvHDT83F7SRTwtSN"
access_token_secret = "0BHBBIPvP25Fxd8O81XCFFBKSIelTaWEsjCcy9p3DU2EH"
consumer_key = "5rmXOhuSBIsBH6ma6pdN9E6l5"
consumer_secret = "aOSREVNHBMvO4zAtrOfvpAbGmty0ba1NI9Mu7MkBcYin569JVc"

_auth = None

def authenticate():
  global _auth 
  if _auth:
      return _auth
  _auth = OAuthHandler(consumer_key, consumer_secret)
  _auth.set_access_token(access_token, access_token_secret)
  return _auth
