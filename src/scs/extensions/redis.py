# -*- coding: utf-8 -*-
"""."""
from flask_redis import FlaskRedis


def bind(app):
    """."""
    return FlaskRedis(app)
