import numpy as np
from PIL import Image
import aircv as ac
import io


def check_config_arguments(key_word: list, config: dict) -> bool:
    check_ok = True
    for i in key_word:
        if i not in config:
            check_ok = False
            break
    return check_ok


def check_var_name(name_: str) -> bool:
    if len(name_) == 0:
        return False
    if name_[0] != '$':
        return False
    return True


def aircv_read_from_array(array_):
    return ac.cv2.imdecode(array_, ac.cv2.IMREAD_COLOR)


def pillow_save_as_array(image_: Image.Image):
    byteio = io.BytesIO()
    image_.save(byteio, 'png')
    
    byteio.seek(0, io.SEEK_SET)
    buff = byteio.read(1024)
    data = b''
    while buff:
        data += buff
        buff = byteio.read(1024)
    barray = np.asarray(bytearray(data), 'uint8')
    return barray
