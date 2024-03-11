import pathlib
import threading
import sys
import pandas as pd
import time
import random
from spiders.base import CrawlerBase
from logger import info_log, error_log
from settings import Config
from spiders.const import LJUrl, LJHtmlSelector, LJCrawlWay, LJOther
from lxml import etree

from concurrent.futures import ThreadPoolExecutor, as_completed
from spiders.exception import ResponseError, HtmlVerificationError
from utils.tools import chinese2pinyin_abbr


class LJXFCrawler(CrawlerBase):
    def __init__(self, _city: str = "cd"):
        super().__init__()
        self.city = _city
        self.filename = self._filename

    def _require(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Referer': 'https://cd.fang.lianjia.com/loupan/'
        }

    @property
    def _filename(self):
        return f'{self.city}_xf_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'

    @staticmethod
    def _extract_first(data):
        if isinstance(data, (list, tuple)):
            data = data[0] if data else ''
        return data

    @staticmethod
    def _join(data):
        if isinstance(data, (list, tuple)):
            data = '，'.join(data)
        return data

    @staticmethod
    def to_excel(save_path: pathlib.Path, data: list, columns: list):
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(save_path, index=False)

    def crawling(self, page: int):
        new_house_url = LJUrl.NEW_HOUSE_DATA_URL.value.format(self.city, page)
        list_resp = self.get(url=new_house_url)
        html_tree = etree.HTML(list_resp.text)

        house_list = html_tree.xpath(LJHtmlSelector.NEW_HOUSE_LIST.value)
        if not house_list:
            raise HtmlVerificationError(f'出现人机验证 >>> {new_house_url=}')  # todo selenium处理

        house_columns = []
        for house in house_list:
            # ------------------------------------------ 楼盘列表 ------------------------------------------
            house_name = self._extract_first(house.xpath(LJHtmlSelector.NEW_HOUSE_NAME.value))  # 楼盘名称
            house_type = self._extract_first(house.xpath(LJHtmlSelector.NEW_HOUSE_TYPE.value))  # 楼盘类型  住宅/公寓
            house_status = self._extract_first(house.xpath(LJHtmlSelector.NEW_HOUSE_STATUS.value))  # 楼盘状态  在售/待售
            house_avg_price = self._extract_first(house.xpath(LJHtmlSelector.NEW_HOUSE_AVG_PRICE.value))  # 楼盘均价 元/平
            house_total_price = self._extract_first(house.xpath(LJHtmlSelector.NEW_HOUSE_TOTAL_PRICE.value))  # 楼盘总价 万/套
            house_detail_url = self._extract_first(house.xpath(LJHtmlSelector.NEW_HOUSE_DETAIL_URL.value))  # 楼盘详情页url
            # ------------------------------------------ 楼盘列表 ------------------------------------------

            # ------------------------------------------ 楼盘详情 ------------------------------------------
            detail_url = LJUrl.NEW_HOUSE_DETAIL_BASE_URL.value.format(self.city, house_detail_url)
            detail_resp = self.get(url=detail_url)
            detail_tree = etree.HTML(detail_resp.text)
            house_address = self._extract_first(detail_tree.xpath(LJHtmlSelector.NEW_HOUSE_ADDRESS.value))  # 项目地址
            house_open_date = self._extract_first(detail_tree.xpath(LJHtmlSelector.NEW_HOUSE_OPEN_DATE.value))  # 最近开盘
            house_type_list = self._join(detail_tree.xpath(LJHtmlSelector.NEW_HOUSE_TYPE_LIST.value))  # 楼盘户型
            # ------------------------------------------ 楼盘详情 ------------------------------------------

            house_item = [
                house_name, house_type, house_status,
                house_avg_price, house_total_price, detail_url,
                house_address, house_open_date, house_type_list
            ]
            house_columns.append(house_item)

        return house_columns

    def crawl_page_async(self, max_page: int, max_num: int):
        info_log.info(f'开始多线程爬取...')
        house_data = []
        with ThreadPoolExecutor(max_workers=LJOther.MAX_WORKERS.value) as executor:
            tasks = [executor.submit(self.crawling, page) for page in range(1, max_page + 1)]
            for future in as_completed(tasks):
                try:
                    page_house = future.result()
                    if not page_house:
                        info_log.info(f'已经爬取到最后一页，爬取结束')
                        break
                    with threading.Lock():
                        if len(house_data) >= max_num:
                            info_log.info(f'已经爬取到最大数量，爬取结束')
                            break
                        house_data.extend(page_house)
                    time.sleep(random.randint(LJOther.RANDOM_RANGE_LEFT.value, LJOther.RANDOM_RANGE_RIGHT.value))
                except (ResponseError, HtmlVerificationError) as e:
                    error_log.error(f'crawl error, {e=}')
                    break
        return house_data

    def crawl_page(self, max_page: int, max_num: int):
        info_log.info(f'开始同步爬取...')
        house_data = []
        curr_page = 1
        while curr_page <= max_page:
            try:
                info_log.info(f'开始爬取第{curr_page}页...')
                page_house = self.crawling(page=curr_page)
                if not page_house:
                    info_log.info(f'已经爬取到最后一页，爬取结束')
                    break
                if len(house_data) >= max_num:
                    info_log.info(f'已经爬取到最大数量，爬取结束')
                    break
                house_data.extend(page_house)
                time.sleep(random.randint(LJOther.RANDOM_RANGE_LEFT.value, LJOther.RANDOM_RANGE_RIGHT.value))
                info_log.info(f'第{curr_page}页爬取完成')
            except (ResponseError, HtmlVerificationError) as e:
                error_log.error(f'crawl error, {e=}')
                break
            curr_page += 1
        return house_data

    def run(self, max_num: int = 1, is_async=False):
        max_page = max_num // LJOther.PER_PAGE.value + 1 \
            if max_num % LJOther.PER_PAGE.value else max_num // LJOther.PER_PAGE.value

        header_columns = ['楼盘名称', '楼盘类型', '楼盘状态', '楼盘均价', '楼盘总价', '楼盘详情']
        detail_header_columns = ['项目地址', '最近开盘', '楼盘户型']
        header_columns.extend(detail_header_columns)

        save_path = pathlib.Path(Config.LJ_NEW_HOUSE_SAVE_DIR).joinpath(self.filename)
        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        if not is_async:  # 同步单线程爬取
            house_data = self.crawl_page(max_page=max_page, max_num=max_num)
        else:  # 多线程爬取
            house_data = self.crawl_page_async(max_page=max_page, max_num=max_num)

        info_log.info(f'爬取完成，共{len(house_data)}条数据，即将写入文件...')
        house_data = house_data[:max_num]
        self.to_excel(save_path=save_path, data=house_data, columns=header_columns)
        info_log.info(f'写入文件完成，文件路径：{save_path}')
        return save_path


def main():
    print("\n==================================================================================")
    city = input('【链家新房】请输入要爬取的城市缩写（例如`重庆`）：')
    city = chinese2pinyin_abbr(city)
    if not city:  # TODO 暂时没有对用户输入对城市进行合法性校验，如果输入城市不存在会导致爬取的数据有误。
        raise ValueError('【链家新房】城市缩写不能为空')

    num = input('【链家新房】请输入要爬取的楼盘数量（默认为1）：')
    if not num: num = LJOther.DEFAULT_CRAWL_NUM.value

    craw_way = input('【链家新房】请选择爬取方式（0：[默认]同步单线程爬取，1：异步多线程爬取）：')
    if not craw_way: craw_way = LJCrawlWay.SINGLE_CRAWL.value
    is_async = True if int(craw_way) == LJCrawlWay.ASYNC_CRAWL.value else False

    print("【链家新房】开始爬取...")
    craw = LJXFCrawler(city)
    craw.run(max_num=int(num), is_async=is_async)
    print("【链家新房】爬取完成...")
    print("==================================================================================\n")


if __name__ == '__main__':
    main()
