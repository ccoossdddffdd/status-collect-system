# -*- coding: utf-8 -*-
"""."""
from flask_caching import Cache


def bind(app):
    """."""
    return Cache(app)
