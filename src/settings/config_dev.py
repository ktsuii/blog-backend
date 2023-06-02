from settings.config_base import Config, env


class ConfigDev(Config):
    ENV_NAME = '开发环境'
    DEBUG = False
