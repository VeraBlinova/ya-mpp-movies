FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings.dev'
ENV TEMPLATE_URL 'http://notifications:8000/Napi/v1/template/'

ADD . /app/
WORKDIR /app/

RUN  pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./entrypoint.sh" ]