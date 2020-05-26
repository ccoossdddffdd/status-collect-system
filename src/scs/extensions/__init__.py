# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

import py
from fs import open_fs


def bind(app):
    """."""
    path_local = py.path.local(__file__)
    fs_handle = open_fs(path_local.dirname)

    for path in fs_handle.walk.files(filter=["*.py"]):
        if path == "/__init__.py":
            continue

        model = path_local.dirpath().join(path).pyimport()
        obj = model.bind(app)
        if obj is not None:
            setattr(app, path.replace("/", "").replace(".py", ""), obj)
