FROM python:3.7-alpine
COPY ./repositories /etc/apk/repositories 

RUN pip install pipenv -i https://mirrors.aliyun.com/pypi/simple/

RUN apk add --update --no-cache gcc libxml2 libxml2-dev make libxslt-dev libffi-dev musl-dev 

COPY ./run_celery.sh /data/
RUN chmod +x /data/run_celery.sh

COPY ./run_gunicorn.sh /data/
RUN chmod +x /data/run_gunicorn.sh

COPY ./run_schedule.sh /data/
RUN chmod +x /data/run_schedule.sh

COPY ./run_pipenv_install.sh /data/
RUN chmod +x /data/run_pipenv_install.sh
