from geopy import distance
import google_maps
import foursquare_api
import heapq
import json
import timeit

class LocationOverlapHandler(object):

  def __init__(self, timespan=1, api=foursquare_api.FoursquareAPI):
    """timespan in hours
      get the event location overlaps within the specified timespan
    """
    self.current_results_dict = {}
    self.map_api = api()

  def get_location_info(self, location_queries):
    for query in location_queries:
      if self.current_results_dict.get(query):
        for address_definition in self.current_results_dict.get(query):
          address_definition['overlap'] = address_definition.get('overlap', 0) + 1
      else:
        new_address_definitions = []
        for address_definitions in self.current_results_dict.values():
          for address in address_definitions:
            if query.lower() in address['formatted_address'].lower():
              new_address_definitions.append(address)
        
        if len(new_address_definitions) == 0:
          address_defs = self.map_api.get_address_definitions(query)
          new_address_definitions.extend(address_defs)

        self.update_location_overlaps(self.current_results_dict, new_address_definitions)
        self.current_results_dict[query] = new_address_definitions

    return self.current_results_dict

  def update_location_overlaps(self, location_queries_dict, new_address_definitions):
    for q1, results1 in location_queries_dict.items():
      overlap_set_old = set()
      overlap_set_new = set()
      for index1, address_def_old in enumerate(results1):
        loc1 = (address_def_old['lat'], address_def_old['lng'])
        for index2, address_def_new in enumerate(new_address_definitions):
          loc2 = (address_def_new['lat'], address_def_new['lng'])
          if distance.great_circle(loc1, loc2).miles <= 1:
            overlap_set_old.add(index1)
            overlap_set_new.add(index2)
        
      for i in list(overlap_set_new):
        new_address_definitions[i]['overlap'] = new_address_definitions[i].get('overlap', 0) + 1
      for i in list(overlap_set_old):
        results1[i]['overlap'] = results1[i].get('overlap', 0) + 1
            
    
    return location_queries_dict

  def get_close_locations(self, location_queries_dict, precision=2):
    coords_dict = {}
    for (query, address_defs) in location_queries_dict.items():
      for address_def in address_defs:
        key = "%f,%f" %(round(float(address_def['lat']), precision), round(float(address_def['lng']), precision))
        coords_dict[key] = coords_dict.get(key, [])
        coords_dict[key].append(address_def)

    return coords_dict 

  def get_best_ranked(self, location_dict, n=3):
    heap = [(entry['overlap'],  entry['formatted_address'], (entry['lat'], entry['lng'])) for entry in location_dict]
    return heapq.nlargest(n, heap)


if __name__ == "__main__":
  # location_queries = ['dolmabahce caddesi', 'vodafone arena', 'tobb', 'tobb ikizler', 'diyanet camisi', 'sogutozu cad', 'besiktas belestepe', 'dolmabahce', 'vodafone arena']
  loc_handler = LocationOverlapHandler()

  # # loc_handler.get_location_info(location_queries)

  with open("location_google.json", 'r', encoding="utf8") as fp:
    location_query_dict = json.load(fp)
  
  coords_dict = loc_handler.get_close_locations(location_query_dict)
  print(coords_dict)
  for c, a in coords_dict.items():
    print(c, len(a))
  # loc_handler.update_location_overlaps()
  # print(loc_handler.current_results_dict)
