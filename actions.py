from base import *
from exceptions import *
import utils
import time
import os

from PIL import ImageGrab
import aircv as ac
import pyautogui


_actions_available = {
    "move_mouse_to",
    "sleep",
    "mouse_click",
    "get_image_pos",
    "screen_shot",
    "remove_file",
    "text_input",
    "text_input_file",
    "screen_shot_mem",
}

_actions_map = dict()


class Action(Base):
    def __init__(self, config_: dict, root_):
        self._root = root_
        self._parse_config(config_)

    def _parse_config(self, config_: dict) -> None:
        pass

    def call(self) -> bool:
        return True


def load_action(action_: dict, root) -> Action:
    key_words = ["type", "action"]
    check = utils.check_config_arguments(key_words, action_)
    if not check:
        raise ParseErrorException("Loading action error, argument missing.")
    if action_["type"] != "action":
        raise ParseErrorException(
            "Loading action error, type error: {}".format(action_["type"])
        )
    if action_["action"] not in _actions_available:
        raise ParseErrorException("Action not support: {}".format(action_["action"]))
    actobj = _actions_map[action_["action"]]
    return actobj(action_, root)


class Action_move_mouse_to(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "var"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_move_mouse_to error, missing argument: var"
            )
        self._var = config_["var"]

    def call(self) -> bool:
        target = self._root.get_var(self._var)
        pyautogui.moveTo(target)
        return True


class Action_sleep(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "sleep_time"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_sleep error, argument missing: sleep_time"
            )
        self._sleep_time = config_["sleep_time"]

    def call(self) -> bool:
        time.sleep(self._sleep_time)
        return True


class Action_mouse_click(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "push_time"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_mouse_click error, missing argument: push_time"
            )
        self._push_time = config_["push_time"]

    def call(self) -> bool:
        pyautogui.mouseDown()
        time.sleep(self._push_time)
        pyautogui.mouseUp()
        return True


class Action_get_image_pos(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "var", "base", "image", "precision"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_get_image_pos error, missing arguments."
            )
        self._var = config_["var"]
        self._base = config_["base"]
        self._image = config_["image"]
        self._precision = config_["precision"]

    def call(self) -> bool:
        # im_src
        if self._base[0] == "$":
            data = self._root.get_var(self._base)
            im_src = utils.aircv_read_from_array(data)
        else:
            im_src = ac.imread(self._base)

        # im_tgt
        if self._image[0] == "$":
            data = self._root.get_var(self._image)
            im_tgt = utils.aircv_read_from_array(data)
        else:
            im_tgt = ac.imread(self._image)
        get = ac.find_template(im_src, im_tgt)
        if get is None:
            return False
        if get["confidence"] < self._precision:
            return False
        self._root.set_var(self._var, get["result"])
        return True


class Action_screen_shot(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "save"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_screen_shot error, missing argument: save"
            )
        self._save = config_["save"]

    def call(self) -> bool:
        img = ImageGrab.grab()
        img.save(self._save)
        return True


class Action_remove_file(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "ignore_error", "path"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_remove_file error, missing arguments."
            )
        self._ignore_error = config_["ignore_error"]
        self._path = config_["path"]

    def call(self) -> bool:
        exists = os.path.exists(self._path)
        if not exists:
            if self._ignore_error:
                return True
            return False
        try:
            os.remove(self._path)
        except:
            if not self._ignore_error:
                return False
        return True


class Action_text_input(Action):
    def __init__(self, config_: dict, root_):
        super().__init__(config_, root_)
        self._key_to_change = {" ": "space"}

    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "text"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_text_input error, missing argument: text"
            )
        self._text = config_["text"]

    def _press_key(self, key: str):
        if len(key) == 0:
            return
        if len(key) > 1:
            key = key[0]
        upper = False
        if key.isupper():
            upper = True
        if upper:
            pyautogui.keyDown("shiftleft")
        k = key
        if k in self._key_to_change:
            k = self._key_to_change[k]
        pyautogui.keyDown(k)
        pyautogui.keyUp(k)
        if upper:
            pyautogui.keyUp("shiftleft")

    def call(self) -> bool:
        for i in self._text:
            self._press_key(i)
        return True


class Action_text_input_file(Action):
    def __init__(self, config_: dict, root_):
        super().__init__(config_, root_)
        self._key_to_change = {" ": "space"}

    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "file"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_text_input error, missing argument: text"
            )
        path = config_["file"]
        with open(path, "r", encoding="utf_8") as f:
            self._text = f.read()

    def _press_key(self, key: str):
        if len(key) == 0:
            return
        if len(key) > 1:
            key = key[0]
        upper = False
        if key.isupper():
            upper = True
        if upper:
            pyautogui.keyDown("shiftleft")
        k = key
        if k in self._key_to_change:
            k = self._key_to_change[k]
        pyautogui.keyDown(k)
        pyautogui.keyUp(k)
        if upper:
            pyautogui.keyUp("shiftleft")

    def call(self) -> bool:
        for i in self._text:
            self._press_key(i)
        return True


class Action_screen_shot_mem(Action):
    def _parse_config(self, config_: dict) -> None:
        key_words = ["type", "action", "var"]
        check = utils.check_config_arguments(key_words, config_)
        if not check:
            raise ParseErrorException(
                "Loading Action_screen_shot_to_mem error, missing argument."
            )
        self._var = config_["var"]

    def call(self) -> bool:
        image = ImageGrab.grab()
        arr = utils.pillow_save_as_array(image)
        self._root.set_var(self._var, arr)
        return True


for i in _actions_available:
    _actions_map[i] = eval("Action_" + i)
