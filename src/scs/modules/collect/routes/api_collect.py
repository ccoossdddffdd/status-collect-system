# -*- coding: utf-8 -*-
import requests
import os
import json
import traceback

from flask import current_app
from flask import request
from logbook import info, warn

@current_app.route("/collect/<group>", methods=['GET'])
def api_collect(group):
    code, msg, data = 1, 'faild', {}
    try:
        key = request.args.get('key', '')
        assert key != '', 'key 值不能为空'

        uuid = request.args.get('uuid', '')
        assert uuid != '', 'uuid 值不能为空'

        collect = current_app.status.loadCollectObject(group, key)
        assert collect is not None, '未设置收集类型'
        
        data = collect.do(uuid)
        code, msg = 0, 'ok'
    except Exception as error:
        code, msg = 99992, 'err: [{}]'.format(error)
        warn(error)
        warn(traceback.format_exc())

    return {
        'code' : code,
        'data': data,
        'msg' : msg,
    }
