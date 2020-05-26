# -*- coding: utf-8 -*-
"""Application configuration."""
from celery.schedules import crontab
from environs import Env

env = Env()
env.read_env()

SECRET_KEY = 'trader-bot'

# amqp://myuser:mypassword@localhost:5672/myvhost
REDIS_URL = env("REDIS_URL", "redis://localhost:6379/0")
CACHE_TYPE = "redis"
CACHE_REDIS_URL = REDIS_URL
CACHE_KEY_PREFIX = 'c|'
CACHE_DEFAULT_TIMEOUT = 120

CELERY_BROKER_URL = REDIS_URL
# CELERY_BROKER_URL = 'amqp://admin:mypass@rabbit:5672/trade_bot'
# CELERY_BROKER_URL = 'amqp://admin:mypass@localhost:5672/trade_bot'
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Asia/Shanghai'

REQUEST_SECRET = env("REQUEST_SECRET", '')
CORE_HOST = env("CORE_HOST", '')
LOG_NAME = env("LOG_NAME", 'pppay-middleware')
LOG_PATH = env("LOG_PATH", '/data/www/logs')
QRCODE_PATH = env("QRCODE_PATH", '/data/www/qrcodes')
QRCODE_URL = env("QRCODE_URL", 'http://QRCODE_URL')

FATEADM_PD_ID = env("FATEADM_PD_ID", '')
FATEADM_PD_KEY = env("FATEADM_PD_KEY", '')
FATEADM_APP_ID = env("FATEADM_APP_ID", '')
FATEADM_APP_KEY = env("FATEADM_APP_KEY", '')

KDL_ORDER_ID = env("KDL_ORDER_ID", '')
KDL_ORDER_APPKEY = env("KDL_ORDER_APPKEY", '')
KDL_LOAD_COUNT = env("KDL_LOAD_COUNT", 1)
PPOOL_MIN = env("KDL_LOAD_COUNT", 1)