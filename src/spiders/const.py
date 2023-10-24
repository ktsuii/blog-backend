from enum import Enum


class ZZZMHUrl(Enum):
    """极简壁纸"""
    LIST_DATA_URL = 'https://api.zzzmh.cn/bz/v3/getData'
    DOWNLOAD_URL = 'https://api.zzzmh.cn/bz/v3/getUrl/{}'
    SEARCH_DATA_URL = 'https://api.zzzmh.cn/bz/v3/searchData'


class LJUrl(Enum):
    """链家"""
    NEW_HOUSE_DATA_URL = 'https://{}.fang.lianjia.com/loupan/pg{}/'
    NEW_HOUSE_DETAIL_BASE_URL = 'https://cd.fang.lianjia.com{}'


class LJHtmlSelector(Enum):
    """链家网页元素选择器"""
    NEW_HOUSE_LIST = "//li[@class='resblock-list post_ulog_exposure_scroll has-results']"
    NEW_HOUSE_NAME = ".//div[@class='resblock-name']/a/text()"
    NEW_HOUSE_TYPE = ".//div[@class='resblock-name']/span[@class='resblock-type']/text()"
    NEW_HOUSE_STATUS = ".//div[@class='resblock-name']/span[@class='sale-status']/text()"
    NEW_HOUSE_AVG_PRICE = ".//div[@class='resblock-price']/div[@class='main-price']/span[@class='number']/text()"
    NEW_HOUSE_TOTAL_PRICE = ".//div[@class='resblock-price']/div[@class='second']/text()"
    NEW_HOUSE_DETAIL_URL = "./a[@class='resblock-img-wrapper ']/@href"
    NEW_HOUSE_ADDRESS = "/html/body/div[2]/div[3]/div[2]/div/div[3]/ul/li[1]/span[2]/text()"
    NEW_HOUSE_OPEN_DATE = "/html/body/div[2]/div[3]/div[2]/div/div[3]/ul/li[2]/div/span[2]/text()"
    NEW_HOUSE_TYPE_LIST = "/html/body/div[2]/div[3]/div[2]/div/div[3]/ul/li[3]/span[2]/span/text()"
