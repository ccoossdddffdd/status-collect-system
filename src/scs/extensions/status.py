# -*- coding: utf-8 -*-
"""."""

import py
import pytz
import sys
import logbook
from logbook import NullHandler, TimedRotatingFileHandler, StreamHandler
from flask import request


class Collect:
    def __init__(self, app, group, key):
        self.app = app
        self.group = group
        self.key = key

    def do(self, uuid):
        pass


class SetCollect(Collect):
    def do(self, uuid):
        """
        设置型
        把状态值设置为正常 or 异常
        """
        status = request.form.get('status', '')
        assert status != '', 'status 值不能为空'


class RunDoneCollect(Collect):
    def do(self, uuid):
        """
        启止型
        第一次触发, 记录开始时间
        第二次触发, 判断执行是否超时, 超时则记录异常
        """
        self.app.cache.get('{}{}{}'.format(self.group, self.key, uuid))


class TriggerCollect(Collect):
    def do(self, uuid):
        """
        触发型
        触发则认为正常
        """
        pass


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
