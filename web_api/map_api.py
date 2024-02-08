
class MapAPI(object):
  def get_address_definitions(self, query):
    """should return possible addresses in a list of dict format
      [{'formatted_address': string, 'lat': float, 'lng': float}]
    """
    raise NotImplementedError()