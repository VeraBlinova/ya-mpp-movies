from django.apps import AppConfig


class CeleryCronConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "celery_cron"
    verbose_name = "Рассылки"
