from database.mysql.mysql_base import mysql_db
from spiders.crawler_base import Crawler


class ProcessLogic:
    def __init__(self):
        self.session_maker = mysql_db.session_maker
        self.crawler = Crawler()
