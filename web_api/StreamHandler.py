from tweepy import OAuthHandler, Stream, StreamListener
import os,sys,inspect
import json
# import location_tagger
from multiprocessing.pool import ThreadPool
from queue import Queue
from foursquare_api import FoursquareAPI
from google_maps import GoogleMapsAPI
import EventDetectionDAO
import threading
import re
import codecs
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import twitter_auth
from ModelTrainer import ModelTrainer
from ConfManager import ConfManager

get_address_definitions = FoursquareAPI().get_address_definitions
# EventDetectionDAO.init()
# get_address_definitions = GoogleMapsAPI().get_address_definitions
def map_api_worker(q):
  while True:
    (location_query, tweet_obj) = q.get()

    address_defs = get_address_definitions(location_query)
    if len(address_defs):
      EventDetectionDAO.save_location_entity(re.sub(r'[^\w]', '', location_query), address_defs, tweet_obj)

    q.task_done()

class StreamHandler(StreamListener):
  def __init__(self):
    # self.location_entity_extractor = location_tagger.get_crf_tagger()
    self.thread_queue = Queue()
    self.conf = ConfManager()
    self.event_classifier = ModelTrainer(self.conf)
    self.event_classifier.load_from_files()

  def on_data(self, data):
    tweet_raw_obj = json.loads(data)
    try:
        text = (tweet_raw_obj['text'].replace('\n', ' '))
    except KeyError:
        return

    screen_name = tweet_raw_obj['user']['screen_name']
    retweet_count = tweet_raw_obj['retweet_count']
    favorite_count = tweet_raw_obj['favorite_count']
    tweet_date = tweet_raw_obj['timestamp_ms']
    tweet_id = tweet_raw_obj['id']

    self.event_classifier.predict(text)
    # tagged = self.location_entity_extractor.tag(text.split(' '))
    # location_sequences = location_tagger.get_location_sequences(tagged)
    # person_entities = [t[0] for t in tagged if t[1] == 'PERSON']
    # print(text)
    
    # if len(location_sequences) > 0:
    #   # TODO also include a event type attribute for the tweet object
    #   tweet_raw_obj['location_entities'] = location_sequences
    #   for s in location_sequences:
    #     self.thread_queue.put((s, tweet_raw_obj))

      # EventDetectionDAO.save(tweet_raw_obj)


  def on_error(self, status):
    print("========================ERROR========================")


if __name__ == "__main__":
  stream_handler = StreamHandler()
  
  # for i in range(4):
  #   t = threading.Thread(target=map_api_worker, args=(stream_handler.thread_queue,))
  #   t.daemon = True
  #   t.start()

  stream = Stream(twitter_auth.authenticate(), stream_handler)
  stream.filter(track=['cadde', 'bulvar', 'de', 'da', 'te'], languages=['tr'])
