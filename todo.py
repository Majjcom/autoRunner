from base import Base
from exceptions import ParseErrorException
import actions
import utils


class Todo(Base):
    def __init__(self, config_=None, root_=None):
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
