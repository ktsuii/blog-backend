"""
极简壁纸-图片爬取
@Author: zzl
@Date: 2023-04-19
"""
from dataclasses import dataclass
from enum import Enum

from base import BaseSpider


class Const(Enum):
    USER_LOGIN = 'https://api.zzzmh.cn/bz/v3/getData'


@dataclass
class PageListReqParam:
    """请求列表数据参数"""
    current: int  # 当前页码
    size: int = 24  # 每页数量
    category: int = 0
    categoryId: int = 0
    color: int = 0
    ratio: int = 0
    resolution: int = 0
    sort: int = 0


class ZZZMHSpider(BaseSpider):

    def _require(self):
        ...

    def _get_list(self):
        ...

    def run(self):
        ...


if __name__ == '__main__':
    ZZZMHSpider().main()
