
def check_config_arguments(key_word: list, config: dict) -> bool:
    check_ok = True
    for i in key_word:
        if i not in config:
            check_ok = False
            break
    return check_ok
