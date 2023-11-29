import re
import time
from typing import List, Tuple, Union

from pypinyin import lazy_pinyin


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


def chinese2pinyin_abbr(city_name):
    """
    将中文城市名转换为拼音首字母简写。

    参数：city_name (str): 要转换的中文城市名。
    返回：str: 中文城市名的拼音首字母简写。

    示例：
    >>> chinese2pinyin_abbr("重庆")
    >>> 'cq'
    """
    pinyin_list = lazy_pinyin(city_name)
    abbr = ''.join([p[0] for p in pinyin_list])
    return abbr
