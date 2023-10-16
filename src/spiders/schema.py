from dataclasses import dataclass


@dataclass
class ZZZMHPageListReqParam:
    """请求列表数据参数"""
    current: int = 1
    size: int = 24
    category: int = 0
    categoryId: int = 0
    color: int = 0
    ratio: int = 0
    resolution: int = 0
    sort: int = 0


@dataclass
class ZZZMHSearchDataReqParam:
    """请求搜索数据参数"""
    current: int = 1
    size: int = 24
    category: int = 0
    categoryId: int = 0
    color: int = 0
    ratio: int = 0
    resolution: int = 0
    sort: int = 0
    keyword: str = ''