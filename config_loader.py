from exceptions import *
import baseobj
import utils
import json


def load_config_file(path: str) -> list:
    data = None
    with open(path, 'r', encoding='utf_8') as f:
        data = json.load(f)
    key_words = [
        'version',
        'checks'
    ]
    check = utils.check_config_arguments(key_words, data)
    if not check:
        raise ParseErrorException('Loading config error, missing argument.')
    if data['version'] != '1.0':
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
    return event_list

