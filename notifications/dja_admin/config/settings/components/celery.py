import os

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
