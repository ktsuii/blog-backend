from dataclasses import dataclass

from spiders.zzzmh import ZZZMHCrawler


@dataclass
class Crawler:

    def __post_init__(self):
        self.zzzmh = ZZZMHCrawler()
