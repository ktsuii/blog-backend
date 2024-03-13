import pathlib
import time
from dataclasses import asdict
from typing import List

from spiders.exception import ResponseError, DownloadResourceError

from spiders.base import CrawlerBase
from logger import info_log, error_log
from settings.config_base import Config
from spiders.const import ZZZMHUrl, ZZZMHOther
from spiders.executor import JSExecutor
from spiders.schema import ZZZMHPageListReqParam, ZZZMHSearchDataReqParam, ZZZMHWallpaperStruct


class ZZZMHCrawler(CrawlerBase):

    def _require(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Referer': 'https://bz.zzzmh.cn/'
        }
        self.js_executor = JSExecutor()

    def crawling(self, page: int, save_dir: pathlib.Path, kw: str) -> List[ZZZMHWallpaperStruct]:
        wallpapers = []

        # 1. request
        if kw:  # 关键词搜索
            param = ZZZMHSearchDataReqParam(current=page, keyword=kw)
            list_resp = self.post(url=ZZZMHUrl.SEARCH_DATA_URL.value, json=asdict(param))
        else:
            param = ZZZMHPageListReqParam(current=page)
            list_resp = self.post(url=ZZZMHUrl.LIST_DATA_URL.value, json=asdict(param))

        # 2. decrypt
        secret_code = list_resp.json()['result']
        decrypt_code = self.js_executor(
            code_path=Config.ZZZMH_DECRYPT_PATH,
            function='zzzmh_decrypt',
            args=[secret_code]
        )

        # 3. picture download link
        list_data = decrypt_code['list']
        for pic in list_data:
            cust_pic_id = f"{pic['i']}{pic['t']}1"
            download_resp = self.get(url=ZZZMHUrl.DOWNLOAD_URL.value.format(cust_pic_id))
            save_path = save_dir.joinpath(f"{cust_pic_id}.jpg")

            wp_item = ZZZMHWallpaperStruct(
                pid=cust_pic_id,
                path=str(save_path),
                download_content=download_resp.content,
                save_path=save_path  # 冗余，只是为了兼容feature
            )
            wallpapers.append(wp_item)

        return wallpapers

    @staticmethod
    def download_picture(save_path: pathlib.Path, download_content: bytes):
        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)

        with open(save_path, 'wb') as f:
            f.write(download_content)
            info_log.info(f'save picture {save_path} success')

    def run(self, keyword=None, max_num=None, save_dir=None):
        if save_dir is None:
            base_dir = pathlib.Path(Config.ZZZMH_SAVE_DIR)
            save_dir = base_dir.joinpath(time.strftime("%Y%m%d%H%M%S", time.localtime()))

        # 计算最大页数
        max_page = max_num // ZZZMHOther.PER_PAGE.value + 1 \
            if max_num % ZZZMHOther.PER_PAGE.value else max_num // ZZZMHOther.PER_PAGE.value

        flag, crawl_wallpapers = True, []
        curr_page = 1
        while curr_page <= max_page:
            try:
                page_wallpapers = self.crawling(page=curr_page, save_dir=save_dir, kw=keyword)
            except ResponseError as e:
                error_log.error(f'crawling page {curr_page} error, {e=}')
                flag = False
                break
            crawl_wallpapers.extend(page_wallpapers)
            if len(crawl_wallpapers) >= max_num:
                info_log.info(f'已经爬取到最大数量，爬取结束')
                break
            curr_page += 1

        # start download
        for cw in crawl_wallpapers[:max_num]:
            download_content = cw.download_content
            save_path = cw.save_path
            if not download_content and not save_path: continue
            try:
                self.download_picture(save_path=save_path, download_content=download_content)
            except Exception as e:
                error_log.error(f'download picture error={e}, skip')
                continue

        return flag, crawl_wallpapers


def main():
    print("\n==================================================================================")
    num = int(input('【极简壁纸】请输入要爬取的壁纸数量（默认是24张）：'))
    keyword = input('【极简壁纸】请输入要爬取的壁纸关键字：')
    print("【极简壁纸】开始爬取...")
    craw = ZZZMHCrawler()
    craw.run(max_num=num, keyword=keyword)
    print("【极简壁纸】爬取完成...")
    print("==================================================================================\n")


if __name__ == '__main__':
    main()
