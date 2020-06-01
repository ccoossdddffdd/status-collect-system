#!/bin/sh
cd /data/scs

    # --worker-class=gevent \
    # --worker-connections=65535 \
export PIPENV_VENV_IN_PROJECT=1
export PYTHONUNBUFFERED=0
exec pipenv run gunicorn \
    --env LOG_NAME=websrv \
    -w 16 --timeout 60 --reload \
    -b 0.0.0.0:5999 autoapp:app