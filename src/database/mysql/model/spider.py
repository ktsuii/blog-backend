from sqlalchemy import Integer, Column, String, Text, SmallInteger
from sqlalchemy.dialects.mysql import INTEGER

from database.mysql.model.base import Base
from utils.tools import current_timestamp


class Wallpaper(Base):
    """壁纸表"""
    __tablename__ = 'wallpaper'
    __table_args__ = {'comment': '壁纸表'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='主键')
    pid = Column('pid', String(50), nullable=False, index=True, comment='壁纸ID')
    path = Column('path', String(300), nullable=True, comment='图片路径')
    is_delete = Column('is_delete', SmallInteger, server_default='0', comment='是否删除，0：正常，1：删除')
    create_time = Column('create_time', INTEGER(unsigned=True), nullable=False, default=current_timestamp,
                         comment='创建时间')
    update_time = Column('update_time', INTEGER(unsigned=True), nullable=False, default=current_timestamp,
                         onupdate=current_timestamp, comment='更新时间')
