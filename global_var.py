from exceptions import *
import utils


_global_var_map = dict()


def get_var(name_: str):
    check = utils.check_var_name(name_)
    if not check:
        raise RunTimeException("Runtime error, var name error.")
    return _global_var_map[name_]


def set_var(name_: str, value_):
    check = utils.check_var_name(name_)
    if not check:
        raise RunTimeException("Runtime error, var name error.")
    _global_var_map[name_] = value_
