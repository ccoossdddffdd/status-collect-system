# -*- coding: utf-8 -*-
"""Application configuration."""
from celery.schedules import crontab
from environs import Env

env = Env()
env.read_env()

SECRET_KEY = 'trader-bot'

# amqp://myuser:mypassword@localhost:5672/myvhost
REDIS_URL = env("REDIS_URL", "redis://scs-redis:6379/0")
CACHE_TYPE = "redis"
CACHE_REDIS_URL = REDIS_URL
CACHE_KEY_PREFIX = 'c|'
CACHE_DEFAULT_TIMEOUT = 120

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Asia/Shanghai'

REQUEST_SECRET = env("REQUEST_SECRET", '')
LOG_NAME = env("LOG_NAME", 'scs')
LOG_PATH = env("LOG_PATH", '/data/logs')
