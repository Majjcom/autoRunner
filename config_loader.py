from exceptions import *
import baseobj
import utils
import json


_version = "1.2"


class Config:
    def __init__(self, events_: list, interval_: float):
        self.events = events_
        self.interval = interval_


def load_config_file(path: str) -> Config:
    data = None
    with open(path, 'r', encoding='utf_8') as f:
        data = json.load(f)
    key_words = [
        'version',
        'interval',
        'checks'
    ]
    check = utils.check_config_arguments(key_words, data)
    if not check:
        raise ParseErrorException('Loading config error, missing argument.')
    if data['version'] != _version:
        raise ParseErrorException('Loading config error, version not match.')
    event_list = list()
    for i in data['checks']:
        key_words = [
            'type',
            'event'
        ]
        check = utils.check_config_arguments(key_words, i)
        if not check:
            raise ParseErrorException('Loading config error, missing argument.')
        if i['type'] != 'event':
            raise ParseErrorException('Loading config error, type error: {}'.format(i['type']))
        if i['event'] not in baseobj.event_available:
            raise ParseErrorException('Loading config error, event not support: {}'.format(i['event']))
        event_list.append(baseobj.event_map[i['event']](i))
    return Config(event_list, data['interval'])

