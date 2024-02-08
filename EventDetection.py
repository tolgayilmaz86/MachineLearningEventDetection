from collections import namedtuple
from Emitter import Emitter
from ConfManager import ConfManager

import pandas as pd

EventStruct = namedtuple('event_data', 'events time latitude longitude diameter count')


class EventDetection(object):

    def __init__(self):
        self.max_event_size = 500
        self.event_structs = []
        self.event_list = []

    def create_emitter(self):
        self.emitter = Emitter()

    def populate_events(self, event_data):
        if len(event_data) > self.max_event_size:
            self.event_structs.pop(0)
        self.event_structs.append(event_data)

    def clear_event_data(self):
        self.event_structs.clear()

    def analyse_event_data(self):
        events = self.evaluate()
        self.emitter.emit_event_rates(events)

    def write_file(self, event_data, path='../resources/event_data.csv'):
        # TODO kaza olup olmadigina gore 1,tweet | 0, tweet diye kaydet
        e = pd.DataFrame({'events': event_data.events, 'time': event_data.time,
                          'latitude': event_data.latitude, 'longitude': event_data.longitude,
                          'diameter': event_data.diameter, 'count': event_data.count})
        e.to_csv(index=False, path_or_buf=path)

    def evaluate(self):
        n = self.max_event_size
        popular_event = 'NO EVENT'
        teror_count = self.event_list.count('TEROR')
        trafik_count = self.event_list.count('TRAFIK')
        deprem_count = self.event_list.count('DEPREM')
        sel_count = self.event_list.count('SEL')
        yangin_count = self.event_list.count('YANGIN')

        terror_rate = teror_count/n
        traffic_rate = trafik_count/n
        flood_rate = sel_count/n
        eq_rate = sel_count/n
        fire_rate = yangin_count/n

        if len(self.event_list) > n:
            self.event_list.pop(0)
            if terror_rate > 0.9:
                popular_event = 'TEROR'
            elif traffic_rate/n > 0.9:
                popular_event = 'TRAFIK'
            elif eq_rate/n > 0.9:
                popular_event = 'DEPREM'
            elif fire_rate/n > 0.9:
                popular_event = 'YANGIN'
            elif flood_rate/n > 0.9:
                popular_event = 'SEL'
        return [int(terror_rate*100),
                int(traffic_rate*100),
                int(flood_rate*100),
                int(eq_rate*100),
                int(fire_rate*100),
                popular_event]
