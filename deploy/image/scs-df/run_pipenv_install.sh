#!/bin/sh
cd /data/scs

export PIPENV_VENV_IN_PROJECT=1
export PYTHONUNBUFFERED=0
exec pipenv install --skip-lock
