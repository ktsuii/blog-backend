import pathlib
from dataclasses import asdict
from spiders.exception import ResponseError

from spiders.base import CrawlerBase
from logger import info_log, error_log
from settings.config_base import Config
from spiders.const import ZZZMHUrl
from spiders.executor import JSExecutor
from spiders.schema import ZZZMHPageListReqParam, ZZZMHSearchDataReqParam


class ZZZMHCrawler(CrawlerBase):

    def _require(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Referer': 'https://bz.zzzmh.cn/'
        }
        self.js_executor = JSExecutor()

    def crawling(self, page: int, save_dir: pathlib.Path, kw: str):
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

        # 3. download picture
        list_data = decrypt_code['list']
        for pic in list_data:
            cust_pic_id = f"{pic['i']}{pic['t']}1"
            download_resp = self.get(url=ZZZMHUrl.DOWNLOAD_URL.value.format(cust_pic_id))

            save_path = save_dir.joinpath(f"{cust_pic_id}.jpg")
            if not save_path.parent.exists():
                save_path.parent.mkdir(parents=True)

            with open(save_path, 'wb') as f:
                f.write(download_resp.content)
                info_log.info(f'save picture {save_path} success')

            wallpapers.append(dict(pid=cust_pic_id, path=str(save_path)))

        return wallpapers

    def run(self, keyword=None, max_page=None, save_dir=None):
        if save_dir is None:
            save_dir = pathlib.Path(Config.ZZZMH_SAVE_DIR)

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
            curr_page += 1

        return flag, crawl_wallpapers


if __name__ == '__main__':
    craw = ZZZMHCrawler()
    craw.run(max_page=2)
