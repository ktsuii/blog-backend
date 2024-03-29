import traceback

import requests
from retrying import retry
from logger import error_log


class BaseSpider:
    def __init__(self, headers=None, timeout=20):
        self.session = requests.Session()
        self.headers = headers or {}
        self.timeout = timeout
        self._require()

    def _require(self):
        raise NotImplementedError("Please implement this method in subclass.")

    def run(self):
        raise NotImplementedError("Please implement this method in subclass.")

    def main(self):
        self.run()
        self.close()

    @retry(wait_random_min=500, wait_random_max=2000, stop_max_attempt_number=3)
    def request(self, method, url, **kwargs):
        headers = {**self.headers, **kwargs.get('headers', {})}
        if not any([method, url]):
            raise ValueError('method and url must be not empty.')
        method = method.lower()
        try:
            response = getattr(self.session, method)(
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            return response
        except Exception as e:
            error_log.error(traceback.format_exc())
            error_log.error(f'Request failed: {e}')
            return None

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def close(self):
        self.session.close()
