import re
import time
from typing import List, Tuple, Union


def extract_ip(address) -> str:
    pattern = re.compile(r'((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)')
    m = pattern.search(address)
    return m.group(0) if m else address


def current_timestamp():
    return int(time.time())


def check_element_len(*ele_list: Union[List, Tuple]):
    flag = True
    length = len(ele_list[0])
    for ele in ele_list:
        if len(ele) != length:
            flag = False
    return flag


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        pass
    return False
