from settings.config_base import Config, env


class ConfigProd(Config):
    ENV_NAME = '生产环境'
    DEBUG = False

