# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

import py
from fs import open_fs
from logbook import info, warn
import traceback


def import_commands(path, app):
    if path.check(dir=1) is not True:
        return

    fs_handle = open_fs(str(path))

    for file_name in fs_handle.walk.files(filter=["*.py"]):
        if file_name == "/__init__.py":
            continue
        model = path.join(file_name).pyimport()
        fn_name = file_name.replace("/", "").replace(".py", "")
        if hasattr(model, fn_name):
            app.cli.add_command(getattr(model, fn_name))


def imports(path, app):
    if path.check(dir=1) is not True:
        return

    fs_handle = open_fs(str(path))
    for file_name in fs_handle.walk.files(filter=["*.py"]):
        if file_name == "/__init__.py":
            continue
        path.join(file_name).pyimport()


def bind(app):
    """."""
    path = py.path.local(__file__).dirpath()

    for mod in open_fs(str(path)).listdir('/'):
        if mod in ['__init__.py', '__pycache__', '.DS_Store']:
            continue

        try:
            model = path.join(mod).pyimport()
            if getattr(model, 'active', False) is not True:
                continue
            import_commands(path.join(mod).join('commands'), app)
            imports(path.join(mod).join('routes'), app)
            imports(path.join(mod).join('tasks'), app)
            imports(path.join(mod).join('model'), app)

        except Exception as error:
            warn('err: {mod}', mod=mod)
            warn(error)
            warn(traceback.format_exc())
