
# -*- coding: utf-8 -*-
import requests
import os
import json
import traceback

from flask import current_app
from flask import request
from logbook import info, warn

@current_app.route("/", methods=['GET'])
def api_welcome():
    code, msg, data = 1, 'faild', {}
    try:
        data['hello'] = 'world'
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
