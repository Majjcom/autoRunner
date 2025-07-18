from exceptions import *
from base import *
import global_var
import utils
import aircv as ac
from todo import Todo

event_available = [
    'image_appear',
    'null'
]
event_map = dict()


class Event(Base):
    def __init__(self, config_: dict):
        self._vars = dict()
        self._rate = 5
        self._last_call = 0
        self._mutithreading = False
        self._todo = Todo()
        self._parse_config(config_)

    def _parse_config(self, config_: dict) -> None:
        pass

    def _event_check(self) -> None:
        pass

    def get_var(self, name_):
        check = utils.check_var_name(name_)
        if not check:
            raise RunTimeException("Runtime error, var name error.")
        if name_[1] == '_':
            return global_var.get_var(name_)
        return self._vars[name_]

    def set_var(self, name_, value_):
        check = utils.check_var_name(name_)
        if not check:
            raise RunTimeException("Runtime error, var name error.")
        if name_[1] == '_':
            global_var.set_var(name_, value_)
        else:
            self._vars[name_] = value_

    def event_call(self):
        self._last_call += 1
        if self._last_call == self._rate:
            self._last_call = 0
            self._event_check()


class Event_null(Event):
    def _parse_config(self, config_: dict) -> None:
        key_words = [
            'type',
            'event',
            'rate',
            'todo'
        ]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException('Object Event parse error, missing argument.')
        self._rate = config_['rate']
        self._todo = Todo(config_['todo'], self)

    def _event_check(self) -> None:
        self._todo.call()


class Event_image_appear(Event):
    def _parse_config(self, config_: dict) -> None:
        key_words = [
            'type',
            'base',
            'image',
            'precision',
            'var',
            'rate',
            'todo'
        ]
        check_ok = utils.check_config_arguments(key_words, config_)
        if not check_ok:
            raise ParseErrorException('Object Event parse error, missing argument.')
        if config_['type'] != 'event':
            raise ParseErrorException('Object Event parse error, type error: {}'.format(config_['type']))
        self._base = config_['base']
        self._image = config_['image']
        self._precision = config_['precision']
        self._var = config_['var']
        self._rate = config_['rate']
        self._todo = Todo(config_['todo'], self)

    def _event_check(self) -> None:
        # im_src
        if self._base[0] == '$':
            data = self.get_var(self._base)
            im_src = utils.aircv_read_from_array(data)
        else:
            im_src = ac.imread(self._base)

        # im_tgt
        if self._image[0] == '$':
            data = self.get_var(self._image)
            im_tgt = utils.aircv_read_from_array(data)
        else:
            im_tgt = ac.imread(self._image)
        get = ac.find_template(im_src, im_tgt)
        if get is None:
            return
        if get['confidence'] < self._precision:
            return
        self.set_var(self._var, get['result'])
        self._todo.call()


for i in event_available:
    event_map[i] = eval("Event_" + i)
