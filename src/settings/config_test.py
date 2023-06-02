from settings.config_base import Config, env


class ConfigTest(Config):
    ENV_NAME = '测试环境'
    DEBUG = False
