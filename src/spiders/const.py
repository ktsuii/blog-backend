from enum import Enum


class ZZZMHUrl(Enum):
    LIST_DATA_URL = 'https://api.zzzmh.cn/bz/v3/getData'
    DOWNLOAD_URL = 'https://api.zzzmh.cn/bz/v3/getUrl/{}'
    SEARCH_DATA_URL = 'https://api.zzzmh.cn/bz/v3/searchData'
