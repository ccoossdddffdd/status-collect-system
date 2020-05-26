#!/bin/sh
cd /data/www/pay-middleware

export PIPENV_VENV_IN_PROJECT=1
export PYTHONUNBUFFERED=0
exec pipenv run celery worker -A autoapp.celery --loglevel=info --autoscale 10,3