import logging.config
import os

from settings import Config

log_level = logging.DEBUG if Config.DEBUG else logging.INFO

log_Config_dict = {
    "version": 1,
    'disable_existing_loggers': False,

    'loggers': {
        'log.debug': {
            'handlers': ['console', 'debug'] if Config.DEBUG else ['debug'],
            'level': logging.DEBUG,
            'propagate': False,  # 是否传递给父记录器
        },
        'log.info': {
            'handlers': ['console', 'info'] if Config.DEBUG else ['info'],
            'level': log_level,
            'propagate': False,  # 是否传递给父记录器
        },
        'log.warn': {
            'handlers': ['console', 'warn'],
            'level': logging.WARN,
            'propagate': False,  # 是否传递给父记录器
        },
        'log.error': {
            'handlers': ['console', 'error'],
            'level': logging.ERROR,
            'propagate': False,  # 是否传递给父记录器
        },
    },

    'handlers': {
        # 输出到控制台
        'console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出到文件
        'debug': {
            'level': logging.DEBUG,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': Config.DebugLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8'
        },
        'info': {
            'level': log_level,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': Config.InfoLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8'
        },
        'warn': {
            'level': logging.WARN,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': Config.WarnLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8'
        },
        'error': {
            'level': logging.ERROR,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': Config.ErrorLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8',
        },
        'access': {
            'level': logging.INFO,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': Config.AccessLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8'
        }
    },
    'formatters': {
        # 标准输出格式
        'standard': {
            'format': '%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: %(message)s',
        }
    }
}

for p in Config.LogPaths:
    os.makedirs(os.path.dirname(p), exist_ok=True)

logging.config.dictConfig(log_Config_dict)

debug_log = logging.getLogger("log.debug")
info_log = logging.getLogger("log.info")
warn_log = logging.getLogger("log.warn")
error_log = logging.getLogger("log.error")


LOG_STDOUT_MAP = {
    'debug': debug_log,
    'info': info_log,
    'warn': warn_log,
    'error': error_log,
}


def log_stdout(loglevel: str, msg: str):  # log 标准输出流统一方法
    # get related log stdout method
    log_stdout_method = getattr(LOG_STDOUT_MAP[loglevel], loglevel)
    # stdout log
    log_stdout_method(msg)
