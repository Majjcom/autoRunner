import threading as _threading
from pprint import pprint
from exceptions import *
import time as _time
import config_loader
from base import *
import global_var
import traceback
import actions
import utils

import aircv as ac


class Todo(Base):
    def __init__(self, config_ = None, root_ = None):
        self._actions = list()
        self._root = root_
        if config_:
            self._parse_config(config_)
    
    def _parse_config(self, config_) -> None:
        key_words = [
            'type',
            'actions'
        ]
        check = utils.check_config_arguments(key_words, config_)
        if config_['type'] != 'todo':
            check = False
        if not check:
            raise ParseErrorException('Object Todo parse error.')
        self._load_actions(config_['actions'])
    
    def _load_actions(self, actions_: list) -> None:
        for action in actions_:
            act = actions.load_action(action, self._root)
            self._actions.append(act)
    
    def call(self) -> None:
        ok = True
        for i in self._actions:
            if ok:
                ok = i.call()
            else:
                break


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


class _Running_thread(_threading.Thread):
    def __init__(self, context_) -> None:
        super().__init__()
        self._context = context_
    
    def run(self):
        try:
            sleep_time = self._context.check_rate
            while not self._context.run_end:
                self._context.call()
                _time.sleep(sleep_time)
        except:
            info = traceback.format_exc()
            print(info, end='')
            self._context.error_occur()
        finally:
            self._context.thread_end()


class RunningContext:
    def __init__(self):
        self.check_rate = 5.0
        self._interval = 5.0
        self._event_pool = list()
        self.run_end = False
        self.thread_ended = False
        self.error_occured = False
    
    def _add_event(self, event_: Event):
        self._event_pool.append(event_)
    
    def load_config(self, config_):
        for i in config_.events:
            self._add_event(i)
        self._interval = config_.interval
        self.check_rate = self._interval

    def run(self):
        runner = _Running_thread(self)
        runner.start()
    
    def call(self):
        for i in self._event_pool:
            evt: Event = i
            evt.event_call()
    
    def end(self):
        self.run_end = True
    
    def thread_end(self):
        self.thread_ended = True
    
    def error_occur(self):
        self.error_occured = True


for i in event_available:
    event_map[i] = eval("Event_" + i)
