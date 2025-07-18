import threading as _threading
import time as _time
import traceback
from event import Event


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
