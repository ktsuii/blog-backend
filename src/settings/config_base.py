import os
import pathlib
from typing import Any, Callable, Optional


def env(name: str,
        default: Any = None,
        dtype: Optional[Callable] = None,
        ) -> Any:
    """
    Args:
        - name: 环境变量名
        - default: 默认值
        - dtype: 数据类型，如果不指定，则不会转换类型，否则按照指定的类型转换
    Returns:
         - Any
    """
    if not (value := os.environ.get(name)):
        value = default
    return dtype(value) if dtype else value


class Config:
    """本项目环境变量配置：几乎所有的配置项都可以从环境变量中获取"""
    # 本项目 - 基础配置
    ENV_NAME = '开发环境'
    DEBUG = False
    PROJECT_NAME = 'blog-backend'
    PROJ_ROOT = pathlib.Path(__file__).parent.parent.parent
    SRC_ROOT = pathlib.Path(__file__).parent.parent
    AccessLogPath = str(PROJ_ROOT.joinpath('logs', 'access.log'))
    DebugLogPath = str(PROJ_ROOT.joinpath('logs', 'debug.log'))
    InfoLogPath = str(PROJ_ROOT.joinpath('logs', 'info.log'))
    WarnLogPath = str(PROJ_ROOT.joinpath('logs', 'warn.log'))
    ErrorLogPath = str(PROJ_ROOT.joinpath('logs', 'error.log'))
    LogPaths = [AccessLogPath, DebugLogPath, InfoLogPath, WarnLogPath, ErrorLogPath]
    PORT = env('PORT', 5000, dtype=int)
    TemplatePath = str(SRC_ROOT.joinpath('template'))

    # 基础组件 - Redis相关配置
    REDIS_HOST = env('REDIS_HOST')
    REDIS_PORT = env('REDIS_PORT')
    REDIS_PASSWORD = env('REDIS_PASSWORD')
    REDIS_KEY_PREFIX = env('REDIS_KEY_PREFIX', 'BLOG')
    REDIS_KEY_EXPIRED = env('REDIS_KEY_EXPIRED', 10 * 60, dtype=int)

    # 基础组件 - MySQL连接地址
    MYSQL_HOST = env('MYSQL_HOST')
    MYSQL_PORT = env('MYSQL_PORT')
    MYSQL_USER = env('MYSQL_USER')
    MYSQL_PASSWORD = env('MYSQL_PASSWORD')
    MYSQL_DATABASE = env('MYSQL_DATABASE', 'blog')
    POOL_RECYCLE = env('POOL_RECYCLE', 3600, dtype=int)
    POOL_PRE_PING = env('POOL_PRE_PING', True, dtype=bool)
    ECHO_SQL = env('ECHO_SQL', True, dtype=bool)

    # 爬虫 - 666资源网相关配置
    resource_six_index_url = "https://666java.com/wp-admin/admin-ajax.php"
    resource_six_user_url = "https://666java.com/user"
    resource_six_username = env('resource_six_username', 'Tsurol')
    resource_six_password = env('resource_six_password', '123456zzl')
