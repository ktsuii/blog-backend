from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.mysql.model.base import Base
from settings import Config


class MysqlDB:
    def __init__(self, host='localhost', port: int = 3306, user='root', password='123456', database='mysql',
                 pool_recycle=600, pool_pre_ping=True):
        self.url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        self.mysql_engine = create_engine(self.url, pool_recycle=pool_recycle, pool_pre_ping=pool_pre_ping,
                                          echo=Config.ECHO_SQL, pool_size=20, max_overflow=80)
        self.session_maker = sessionmaker(self.mysql_engine, expire_on_commit=False)
        self.metadata = Base.metadata

    def init_db(self, create_tables=False, drop_before_init=False):
        """初始化Mysql数据库"""
        self.create_tables(create_tables=create_tables, drop_before_init=drop_before_init)

    def create_tables(self, create_tables=False, drop_before_init=False):
        if not create_tables:
            return
        with self.mysql_engine.begin() as conn:
            if drop_before_init:
                self.metadata.drop_all(conn)
            self.metadata.create_all(conn)


MYSQL_CONFIG = {
    'host': Config.MYSQL_HOST,
    'port': Config.MYSQL_PORT,
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'database': Config.MYSQL_DATABASE,
    'pool_recycle': Config.POOL_RECYCLE,
    'pool_pre_ping': Config.POOL_PRE_PING
}
mysql_db = MysqlDB(**MYSQL_CONFIG)
