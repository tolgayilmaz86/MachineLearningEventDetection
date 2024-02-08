import csv
import json
from jellyfish import damerau_levenshtein_distance
from tweepy import Stream
from tweepy import StreamListener
import os, re, string, codecs
from ConfManager import ConfManager
from Preprocessor import Preprocessor
# get district list as a hashmap city-{district set}
# get location phrase rules as a set
# check whether tweet text contains these rules


def clean_tweet(tweet):
    return Preprocessor.clean_tweet(tweet)


def get_district_list(path=ConfManager.location_ilceler):
  district_list = []
  with codecs.open(path, 'r', encoding='utf8') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
      district_list.append(row[0])
    
  return district_list


def get_adverbs(path="zarflar.txt"):
  rules = set()
  with open(path, 'r') as f:
    for line in f:
      line = clean_tweet(line)
      rules.add(line.lower())

  return rules

class LocationDetector(object):
  def __init__(self, 
                districts_path= os.path.join(os.path.dirname(__file__), ConfManager.location_ilceler),
                adverbs_path=os.path.join(os.path.dirname(__file__), ConfManager.location_zarflar)):
    self.district_dict = get_district_list(path=districts_path)
    self.adverbs = get_adverbs(path=adverbs_path)

  def get_location_tags(self, text):
    text = clean_tweet(text)
    text = text.lower()
    tags = []
    window = []
    for index, word in enumerate(text.split()):
      for adverb in self.adverbs:
        try:
          if word == adverb:
            start = index-2
            if start < 0: 
              start = 0 
            tags.append(text.split()[start:index+1])
            break
        except Exception:
          pass
      for (city, districts) in self.district_dict.items():
        if word == city:
          tags.append(city)
        # for district in districts:
        #     if word == district:
        #       tags.append(district)
    
    return tags

class listener(StreamListener):
  location_detector = LocationDetector()

  def on_data(self, status):
    text = json.loads(status).get('text', '')
    # tags = listener.location_detector.get_location_tags(text)
    tags = ct.tag_sents([text.split()])
    locations = []
    for tuples in tags[0]:
      location = []
      if tuples[1] in set(['LOCATION']):
        location.append(tuples[0])
      if len(location):
        locations.append(location)
        print(location)
      

  
  def on_error(self, status_code):
    if status_code == 420:
      #returning False in on_data disconnects the stream
      return False

if __name__ == '__main__':
  import twitter_auth
  # loc_detect = LocationDetector()
  # loc_detect.get_location_tags('ataturk hastanesi yonunde bir kaza var')
  print(os.path.basename(__file__))
  stream = Stream(twitter_auth.authenticate(), listener())
  stream.filter(track=["u", 't'], languages=['tr'])

  

    


