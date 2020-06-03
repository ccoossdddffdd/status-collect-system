# -*- coding: utf-8 -*-
"""."""

import py
import pytz
import sys
import arrow
from flask import request
from scs.utils.fn import now_ts, ts2humanize
from logbook import info, warn


class Collect:
    def __init__(self, app, group, key):
        self.app = app
        self.group = group
        self.key = key

    def do(self, uuid):
        if self.trigger(uuid):
            self.watchdog()
        return []

    def watchdog(self):
        """
        投喂给看门狗的粮食列表
        """
        wd_key = 'scs|wd'
        if not self.app.redis.sismember(wd_key, self.group):
            self.app.redis.sadd(wd_key, self.group)

    def store_status(self, uuid, status):
        """
        status: 
            0: 正常
            1: 异常
        """
        gkey = 'scs|g|{}'.format(self.group)
        if not self.app.redis.sismember(gkey, self.key):
            self.app.redis.sadd(gkey, self.key)

        kkey = 'scs|ks|{}:{}'.format(self.group, self.key)
        kval = self.app.redis.get(kkey)
        if kval is None:
            # 之前没有设置过
            self.app.redis.set(kkey, status)
        else:
            # or 前值正常, 当前值异常
            # TIPS: 前置异常, 则不再更新
            kval = int(kval)
            if kval == 0 and status == 1:
                self.app.redis.set(kkey, 1)

        # 追加异常记录列表
        if status == 1:
            fkkey = 'scs|fk|{}:{}'.format(self.group, self.key)
            self.app.redis.lpush(fkkey, ts2humanize(now_ts()))
            if self.app.redis.llen(fkkey) > 10:
                self.app.redis.rpop(fkkey)

class SetCollect(Collect):
    def trigger(self, uuid):
        """
        设置型
        把状态值设置为正常 or 异常
        """
        status = request.form.get('status', '')
        assert status != '', 'status 值不能为空'

        self.store_status(uuid, int(status))
        return True


class TriggerCollect(Collect):
    def trigger(self, uuid):
        """
        触发型
        触发则认为正常
        """
        self.store_status(uuid, 0)
        return True


class RunDoneCollect(Collect):

    def get_ckey(self, uuid):
        return 'scs|tmp|{}:{}:{}'.format(self.group, self.key, uuid)

    def trigger(self, uuid):
        """
        启止型
        第一次触发, 记录开始时间
        第二次触发, 判断执行是否超时, 超时则记录异常
        """
        ckey = self.get_ckey(uuid)

        store_ts = self.app.redis.get(ckey)
        now = now_ts()

        if store_ts is None:
            self.app.redis.set(ckey, now)
        
        else:
            self.app.redis.delete(ckey)

            store_ts = float(store_ts.decode('utf-8'))

            # x 秒内触发, 则认为正常
            if (now - store_ts) < 10:
                self.store_status(uuid, 0)
            else:
                self.store_status(uuid, 1)
        
        return True

class StatusFactory:
    def __init__(self, app):
        self.app = app

    def loadCollectObject(self, group, key):
        return RunDoneCollect(self.app, group, key)
        
    def loadCollectResult(self, group):
        data = {}
        data['group_name'] = 'group_name: ' + group

        data['items'] = []

        # 查 group 下的 key 列表
        gkey = 'scs|g|{}'.format(group)
        for key in self.app.redis.smembers(gkey):
            key = key.decode('utf-8')

            # 查每个 key 的结果信息
            kkey = 'scs|ks|{}:{}'.format(group, key)
            st = self.app.redis.get(kkey)
            if st is None:
                st = b'1'
            
            # 查每个 key 的异常记录
            fkkey = 'scs|fk|{}:{}'.format(group, key)
            fks = self.app.redis.lrange(fkkey, 1, 50)
            if fks is None:
                fks = []

            data['items'].append({
                'name': 'KEY: {}'.format(key),
                'key': key,
                'status': int(st.decode('utf-8')),
                'trigger_at': [i.decode('utf-8') for i in fks]
            })

        return data

def bind(app):
    """."""
    return StatusFactory(app)
