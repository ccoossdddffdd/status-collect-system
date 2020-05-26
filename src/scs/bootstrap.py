# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from scs import extensions, modules
from celery import bootsteps


def create_app(config_object="scs.settings"):
    """
    An application factory
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__, instance_relative_config=True, template_folder="templates")
    app.config.from_object(config_object)

    with app.app_context():
        extensions.bind(app)
        modules.bind(app)

    return app
