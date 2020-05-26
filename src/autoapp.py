#!/usr/bin/env python
import scs
from scs.bootstrap import create_app

app = application = create_app()
celery = app.celery