import requests
from retrying import retry
from spiders.exception import ResponseError


class CrawlerBase:
    def __init__(self, headers=None, timeout=20):
        self.session = requests.Session()
        self.headers = headers or {}
        self.timeout = timeout
        self._require()

    def _require(self):
        ...

    def run(self):
        raise NotImplementedError("Please implement this method in subclass.")

    @retry(wait_random_min=500, wait_random_max=2000, stop_max_attempt_number=3)
    def request(self, method, url, **kwargs):
        headers = {**self.headers, **kwargs.get('headers', {})}
        if not any([method, url]):
            raise ValueError('method and url must be not empty.')
        method = method.lower()
        response = getattr(self.session, method)(
            url=url,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )
        if response.status_code != 200:
            raise ResponseError(response.status_code, response.text)

        return response

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
