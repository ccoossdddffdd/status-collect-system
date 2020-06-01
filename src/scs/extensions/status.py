# -*- coding: utf-8 -*-
"""."""

import py
import pytz
import sys
import arrow
import logbook
from logbook import NullHandler, TimedRotatingFileHandler, StreamHandler
from flask import request
from scs.utils.fn import now_ts


class Collect:
    def __init__(self, app, group, key):
        self.app = app
        self.group = group
        self.key = key

    def do(self, uuid):
        self.trigger(uuid)
        self.watchdog_uuid(uuid)

    def watchdog_uuid(self, uuid):
        """
        看门狗, 超时未触达, 则记录异常
        """
        pass

    def store_status(self, uuid, status):
        """
        status: 
            0: 正常
            1: 异常
        """
        pass


class SetCollect(Collect):
    def trigger(self, uuid):
        """
        设置型
        把状态值设置为正常 or 异常
        """
        status = request.form.get('status', '')
        assert status != '', 'status 值不能为空'

        self.store_status(uuid, int(status))


class TriggerCollect(Collect):
    def trigger(self, uuid):
        """
        触发型
        触发则认为正常
        """
        self.store_status(uuid, 0)


class RunDoneCollect(Collect):

    def get_ckey(self, uuid):
        return '{}{}{}'.format(self.group, self.key, uuid)

    def trigger(self, uuid):
        """
        启止型
        第一次触发, 记录开始时间
        第二次触发, 判断执行是否超时, 超时则记录异常
        """
        ckey = self.get_ckey(uuid)

        store_ts = self.app.cache.get(ckey)

        if store_ts is None:
            self.app.cache.set(ckey, now_ts())
        
        else:
            if (now_ts() - int(store_ts)) < 10:
                self.store_status(uuid, 0)
            else:
                self.store_status(uuid, 1)



class StatusFactory:
    def __init__(self, app):
        self.app = app

    def loadCollectObject(self, group, key):
        return RunDoneCollect(self.app, group, key)
        
    # def loadCollectResult(self, group, key):
    #     return RunDoneCollect(self.app, group, key)
        
def bind(app):
    """."""
    return StatusFactory(app)
