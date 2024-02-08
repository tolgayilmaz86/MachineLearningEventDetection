from map_api import MapAPI
import requests
import json


class FoursquareAPI(MapAPI):
  client_id = 'EZHLGDR0DQPLHMG4HK4PVMR2AA2X51ZZSHPCZTMR1WNH2IH2'
  client_key = 'RVIHL21GQ3Q34NDFRZCACWAVUK41FKOU3WQ4UT0R5XZTQPC3'

  def explore(self, query):
    url = 'https://api.foursquare.com/v2/venues/explore?query=%s&near=TR&intent=match&client_id=%s&client_secret=%s&v=20170101&limit=10' \
          %(query, self.client_id, self.client_key)
    response = requests.get(url)

    response_body = json.loads(response.text)['response']
    return response_body

  def get_address_definitions(self, query):
    response_body = self.explore(query)
    items = response_body['groups'][0]['items']
    address_defs = []
    for item in items:
      location = item['venue']['location']
      address_defs.append(
        {
          'formatted_address': ' '.join(location['formattedAddress']),
          'lat': location['lat'],
          'lng': location['lng']
        });
    return address_defs
    

if __name__ == '__main__':
  fs_api = FoursquareAPI()
  print(fs_api.get_address_definitions("El Bab"))