import pathlib
from dataclasses import asdict

from base import CrawlerBase
from logger import info_log
from settings.config_base import Config
from spiders.const import ZZZMHUrl
from spiders.executor import JSExecutor
from spiders.schema import ZZZMHPageListReqParam
from exception import ResponseError


class ZZZMHCrawler(CrawlerBase):

    def _require(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Referer': 'https://bz.zzzmh.cn/'
        }
        self.js_executor = JSExecutor()

    def crawling(self, page: int):
        # 1. request
        param = ZZZMHPageListReqParam(current=page)
        list_resp = self.post(url=ZZZMHUrl.LIST_DATA_URL.value, json=asdict(param))
        assert list_resp.status_code == 200, ResponseError(list_resp.status_code, list_resp.text)
        info_log.info(f'get page {page} success')

        # 2. decrypt
        secret_code = list_resp.json()['result']
        decrypt_code = self.js_executor(
            code_path=Config.ZZZMH_DECRYPT_PATH,
            function='zzzmh_decrypt',
            args=[secret_code]
        )
        current_page = decrypt_code['currPage']
        info_log.info(f'decrypt page {current_page} success')

        # 3. download picture
        list_data = decrypt_code['list']
        for pic in list_data:
            cust_pic_id = f"{pic['i']}{pic['t']}1"
            download_resp = self.get(url=ZZZMHUrl.DOWNLOAD_URL.value.format(cust_pic_id))

            assert download_resp.status_code == 200, ResponseError(download_resp.status_code, download_resp.text)

            save_path = pathlib.Path(Config.ZZZMH_SAVE_DIR, f'page{str(current_page)}', f"{cust_pic_id}.jpg")
            if not save_path.parent.exists():
                save_path.parent.mkdir(parents=True)

            with open(save_path, 'wb') as f:
                f.write(download_resp.content)
                info_log.info(f'save picture {save_path} success')

    def run(self, max_page=10):
        curr_page = 1
        while curr_page <= max_page:
            info_log.info(f'start crawling page {curr_page}...')
            self.crawling(page=curr_page)
            info_log.info(f'crawling page {curr_page} success')
            curr_page += 1

        info_log.info('crawling finish')


if __name__ == '__main__':
    craw = ZZZMHCrawler()
    craw.run(max_page=2)
