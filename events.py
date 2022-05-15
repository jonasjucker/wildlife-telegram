import time
import logging
import os

class EventHandler():

    def __init__(self,photos,videos,test):
        self.photos = photos
        self.videos = videos
        self.test = test

    def new_record_name(self,suffix,type):
        event = self._event_name()
        return self._concat_name(event,suffix,type)

    def strip(self,event_path):
        return event_path.split("/")[-1]

    def new_test_record_name(self,suffix,type):
        event = self.test
        return self._concat_name(event,suffix,type)

    def list(self,type,ignore=None):
        if type == 'v':
            abs_to_event = os.path.abspath(self.videos)
            events = os.listdir(self.videos)
        elif type == 'p':
            abs_to_event = os.path.abspath(self.photos)
            events = os.listdir(self.photos)
        else:
            raise ValueError('Unknown suffix for event')

        if ignore:
            for i in ignore:
                try:
                    events.remove(i)
                except ValueError as e:
                    logging.warning(f'List events: {e}')

        return [os.path.join(abs_to_event,event) for event in events]

    def _concat_name(self,event,suffix,type):
        name = self._record_name()
        if type == 'v':
            path = os.path.join(self.videos,event)
        elif type == 'p':
            path = os.path.join(self.photos,event)
        else:
            raise ValueError('Unknown suffix for record')
        os.makedirs(path,exist_ok=True)

        name = f'{name}.{suffix}'
        name = os.path.join(path,name)

        return name

    def _event_name(self):
        time.strftime('%Y-%m-%d_%H', time.localtime())
        return time.strftime('%Y-%m-%d_%H', time.localtime())
    def _record_name(self):
        return time.strftime('%M:%S', time.localtime())

