# -*- coding: utf-8 -*-
"""."""

import py
import pytz
import sys
import logbook
from datetime import datetime
from logbook import NullHandler, TimedRotatingFileHandler, StreamHandler


def utc_tz():
    return datetime.now(tz=pytz.timezone('Asia/Shanghai'))


class LoggerFactory:
    root = None

    def __init__(self, root):
        if root != '':
            self.root = py.path.local(root)

        logbook.set_datetime_format(utc_tz)

        NullHandler().push_application()
        sh = StreamHandler(sys.stdout)
        sh.format_string = '[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] {record.level_name}: {record.message}'
        sh.push_application()

    def loadCollectType(self, group, key):
        pass
        # if self.root is None:
        #     return
        # fh = TimedRotatingFileHandler(self.root.join('{}.log'.format(log_name.replace('/', '-'))))
        # fh.format_string = '[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] {record.level_name}: {record.message}'
        # fh.push_application()


def bind(app):
    """."""
    lf = LoggerFactory(app.config['LOG_PATH'])
    lf.set_logger(app.config.get('LOG_NAME', 'scs'))
    return lf
