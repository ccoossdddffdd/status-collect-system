
# -*- coding: utf-8 -*-
import requests
import os
import json
import traceback

from flask import current_app
from flask import request
from logbook import info, warn

from flask_cors import cross_origin

@current_app.route("/report/<group>", methods=['GET'])
@cross_origin()
def api_report(group):
    code, msg, data = 1, 'faild', {}
    try:
        data['group_name'] = 'group_name: ' + group

        data['items'] = []
        data['items'].append({
            'name': 'fffs asdf',
            'key': 'dihjhgvbhuyghasffe',
            'status': 0,
            'trigger_at': []
        })
        data['items'].append({
            'name': 'fffsasd 手动阀是',
            'key': 'ffhersdfasdg',
            'status': 1,
            'trigger_at': [
                '2020-02-02 21:22:22'
            ]
        })
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
