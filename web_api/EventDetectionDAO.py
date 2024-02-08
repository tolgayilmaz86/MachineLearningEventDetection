from pymongo import MongoClient
import time
import LocationOverlapHandler
import codecs, json

_db = None

def init():
  global _db
  if not _db:
    _db = MongoClient('mongodb://localhost:27017/').eventdetection_database

def save(doc, collection='tweet_with_event'):
  _db[collection].insert_one(doc)

def save_all(docs, collection='tweet_with_event'):
  _db[collection].insert_many(docs)

def save_location_entity(location_query, address_defs, tweet_obj):
  d = {
    location_query: address_defs, 
    'tweet_id': tweet_obj['id'], 
    'timestamp': tweet_obj['timestamp_ms']
    }
    
  collection = 'location_entity'
  _db[collection].insert_one(d)

def get_last_docs_in(collection, minutes=1):
  t_ms = int(time.time()*1000)

  from_time = t_ms - 60*minutes*1000
  print(from_time)

  return _db[collection].find({"timestamp_ms": {"$gte": str(from_time)}})

if __name__ == "__main__":

  cursor = get_last_tweets_in(180)
  loh = LocationOverlapHandler.LocationOverlapHandler()
  for document in cursor:
    location_entities = document.get('location_entities')
    loh.get_location_info(location_entities)

  print(loh.current_results_dict)
  with codecs.open('overlap_result.json', mode="w", encoding="utf8") as f:
    json.dump(loh.current_results_dict, f)