from celery import shared_task
from celery_cron.email_sender import get_sender


@shared_task(name="sender_email")
def sender_email(*args, **kwargs):
    result = get_sender(**kwargs)
    return result
