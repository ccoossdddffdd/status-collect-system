# -*- coding: utf-8 -*-
"""."""
from flask_cors import CORS


def bind(app):
    """."""
    return CORS(app, resources={r"*": {"origins": "*"}})
