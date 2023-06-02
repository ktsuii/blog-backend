import os

"""
需要在环境变量中设置LOCAL_ENV，否则默认读取develop中的配置文件，注意事项：
    * 1、优先读取环境变量中的值
    * 2、k8s部署方式需要在yaml指定
"""
env = os.getenv("LOCAL_ENV", "develop").lower()
if env == 'develop':
    from settings.config_dev import ConfigDev as Config

elif env == 'product':
    from settings.config_prod import ConfigProd as Config

elif env == 'test':
    from settings.config_test import ConfigTest as Config
