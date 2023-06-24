from settings.config_base import Config, env


class ConfigDev(Config):
    ENV_NAME = '开发环境'
    DEBUG = False
    MYSQL_HOST = env('MYSQL_HOST', 'localhost')
    MYSQL_PORT = env('MYSQL_PORT', 3306, dtype=int)
    MYSQL_USER = env('MYSQL_USER', 'root')
    MYSQL_PASSWORD = env('MYSQL_PASSWORD', 'rootzzl123')
    MYSQL_DATABASE = env('MYSQL_DATABASE', 'blog')
    POOL_RECYCLE = env('POOL_RECYCLE', 3600, dtype=int)
    POOL_PRE_PING = env('POOL_PRE_PING', True, dtype=bool)
    ECHO_SQL = env('ECHO_SQL', True, dtype=bool)
