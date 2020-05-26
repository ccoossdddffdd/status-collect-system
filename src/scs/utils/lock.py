from flask import current_app
from time import time


def locker(key, timeout=180):
    """ 锁 3 分钟"""
    key = 'lock::{}'.format(key)
    ret = current_app.redis.set(key, '{}'.format(time()), ex=timeout, nx=True)
    return ret


def locker_release(key):
    key = 'lock::{}'.format(key)
    current_app.redis.delete(key)