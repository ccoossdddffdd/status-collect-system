
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
        data = current_app.status.loadCollectResult(group)
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
