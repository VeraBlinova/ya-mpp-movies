FROM python:3.11.5

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN  apt update && apt install gcc && pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY ./src ./

CMD gunicorn --bind 0.0.0.0:${FLASK_PORT} ${FLASK_APP}:app
