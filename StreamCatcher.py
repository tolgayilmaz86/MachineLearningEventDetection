import tweepy
from tweepy import OAuthHandler

import json
from EventDetection import EventDetection
from EventDetection import EventStruct
from Emitter import Emitter
from Preprocessor import Preprocessor
from ModelTrainer import ModelTrainer
from ConfManager import ConfManager
# from LocationDetection import LocationDetector


class StreamCatcher(tweepy.StreamingClient):

    def __init__(self, conf):
        self.preprocessor = Preprocessor()
        self.stream = None
        self.event_detector = EventDetection()
        self.count = 0
        self.conf = conf

    def set_model(self, model):
        self.model = model

    def create_emitter(self):
        self.emitter = Emitter()

    def on_data(self, data):
        tweet_obj = list()
        tweet_raw_obj = json.loads(data)
        try:
            text = self.preprocessor.removeNewLines(tweet_raw_obj['text'])
        except KeyError:
            return

        screen_name = tweet_raw_obj['user']['screen_name']
        retweet_count = tweet_raw_obj['retweet_count']
        favorite_count = tweet_raw_obj['favorite_count']
        tweet_date = tweet_raw_obj['timestamp_ms']
        tweet_id = tweet_raw_obj['id']

        tweet_obj.append(screen_name)
        tweet_obj.append(retweet_count)
        tweet_obj.append(favorite_count)
        tweet_obj.append(tweet_date)
        tweet_obj.append(text)

        self.count += 1
        if self.count % 20 == 0:
            self.event_detector.analyse_event_data()

        # self.model.test_tweets.append(tweet_obj)

        # print(screen_name, " ---- ", retweet_count, " -- ", favorite_count, " -- ", tweet_date, " -- ", text)
        # location_detector = LocationDetector()
        # location_tags = location_detector.get_location_tags(text)
        # if len(location_tags):
        #     print(location_tags)
        #     predictions = self.model.predict(text, 'sgd')
        self.event_detector.event_list.extend(self.model.predict(text))

        # e = EventStruct(events=event_list, latitude='', longitude='', time=tweet_date, diameter=1, count=1)
        # self.event_detector.write_file(event_data=e)

        return True

    def on_error(self, status):
        print(status)

    def authenticate(self):
        auth = OAuthHandler(self.conf.consumer_key, self.conf.consumer_secret)
        auth.set_access_token(self.conf.access_token, self.conf.access_token_secret)
        return auth

    def start(self):
        stream = tweepy.Stream(self.authenticate(), self)
        stream.filter(track=['a', 'u', 'e', 'i', 'n', 'd', 'r'], languages=['tr'])

# if __name__ == '__main__':
#     streamCatcher = StreamCatcher()
#     stream = Stream(streamCatcher.authenticate(), streamCatcher)
#     stream.filter(track=['a', 'u', 'e', 'i', 'n', 'd', 'r'], languages=['tr'])
