#!/bin/sh
cd /data/www/pay-middleware

export PIPENV_VENV_IN_PROJECT=1
export PYTHONUNBUFFERED=0
exec pipenv install --skip-lock
