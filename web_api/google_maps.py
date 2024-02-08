from map_api import MapAPI
import requests
from geopy import distance
from collections import namedtuple
import heapq
import json
import codecs
import LocationOverlapHandler



class GoogleMapsAPI(MapAPI):
  api_key = "AIzaSyB0IhqKjKUFeeO_R7ItLjq2f61h8gX4Q70"
  
  def get_textsearch(self, keyword):
    return requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s" %(keyword, self.api_key))

  def get_autocomplete(self, query):
    return requests.get("https://maps.googleapis.com/maps/api/place/autocomplete/json?input=%s&location=%s&key=%s" %(query, '39.9065009,32.7609194', self.api_key))

  def get_coordinates_from_id(self, place_id):
    print("https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" %(place_id, api_key))
    return requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" %(place_id, self.api_key))

  def get_address_definitions(self, query):
    response = self.get_textsearch(query)
    address_defs = []
    for result in response.json()['results']:
      address_def = {
        "formatted_address": result['formatted_address'],
        "lat": result['geometry']['location']['lat'],
        "lng": result['geometry']['location']['lng']
        }
      address_defs.append(address_def)
    
    return address_defs

if __name__ == "__main__":
  api = GoogleMapsAPI()

  defs = api.get_address_definitions("Suriye El Bab")
  print(defs)