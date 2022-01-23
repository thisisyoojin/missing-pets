FROM python:latest

COPY . /app

RUN python -m pip install --upgrade pip \
    pip install -r app/requirements.txt

ENTRYPOINT python app/aws_cron/app.py
