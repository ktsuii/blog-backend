from sqlalchemy import Integer, Column, String, Text, SmallInteger
from sqlalchemy.dialects.mysql import INTEGER

from database.mysql.model.base import Base
from utils.tools import current_timestamp


class Article(Base):
    """文章表"""
    __tablename__ = 'article'
    __table_args__ = {'comment': '文章表'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='主键')
    title = Column('title', String(100), nullable=False, comment='标题')
    content = Column('content', Text, nullable=False, comment='内容')
    author = Column('author', String(50), nullable=False, comment='作者')
    description = Column('description', String(500), nullable=True, comment='简述')
    cover_path = Column('cover_path', String(300), nullable=True, comment='封面图片路径')
    is_delete = Column('is_delete', SmallInteger, server_default='0', comment='是否删除，0：正常，1：删除')
    create_time = Column('create_time', INTEGER(unsigned=True), nullable=False, default=current_timestamp,
                         comment='创建时间')
    update_time = Column('update_time', INTEGER(unsigned=True), nullable=False, default=current_timestamp,
                         onupdate=current_timestamp, comment='更新时间')
