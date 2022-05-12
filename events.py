import time
import os

def new_record_name(suffix,type):
    event = _event_name()
    return _concat_name(event,suffix,type)

def new_test_record_name(suffix,type):
    event = 'test'
    return _concat_name(event,suffix,type)

def _concat_name(event,suffix,type):
    name = _record_name()
    if type == 'v':
        path = os.path.join('videos',event)
    elif type == 'p':
        path = os.path.join('photos',event)
    else:
        raise ValueError('Unknown suffix for record')
    os.makedirs(path,exist_ok=True)

    name = f'{name}.{suffix}'
    name = os.path.join(path,name)

    return name

def _event_name():
    time.strftime('%Y-%m-%d_%H', time.localtime())
    return time.strftime('%Y-%m-%d_%H', time.localtime())
def _record_name():
    return time.strftime('%M:%S', time.localtime())
