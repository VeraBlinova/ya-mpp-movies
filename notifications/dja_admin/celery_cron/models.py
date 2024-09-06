import json
from datetime import datetime, timedelta

from django.db import models
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from .tasks import sender_email


class BaseNotif(models.Model):

    class channeltype(models.TextChoices):
        EMAIL = "email"
        PUSH = "push"

    channel = models.CharField("Способ доставки", choices=channeltype.choices)
    msg_to = models.CharField("Адресаты", max_length=50)
    msg_subj = models.CharField("Тема", max_length=50)
    template_id = models.UUIDField("Шаблон", max_length=50)
    template_data = models.TextField("Данные шаблона", max_length=500)

    class Meta:
        abstract = True

    def __init__(self):
        self.kwargs = None
        self.task = None

    def get_channel(self):
        if self.channel == "email":
            self.task = "sender_email"
        self.kwargs = json.dumps(
            {
                "msg_to": self.msg_to,
                "msg_subj": self.msg_subj,
                "template_id": str(self.template_id),
                "template_data": self.template_data,
            }
        )


class Notif(BaseNotif, ClockedSchedule):

    class Meta:
        verbose_name_plural = "Рассылки"

    def save(self, **kwargs):
        self.get_channel()
        self.clocked_time = datetime.now() + timedelta(seconds=10)
        super().save(**kwargs)  # Call the "real" save() method.


class LateNotif(BaseNotif, ClockedSchedule):

    class Meta:
        verbose_name_plural = "Отложенные рассылки"

    def save(self, **kwargs):
        self.get_channel()
        super().save(**kwargs)


class PereodicNotif(BaseNotif, PeriodicTask):

    class Meta:
        verbose_name_plural = "Переодические рассылки"

    def save(self, **kwargs):
        self.get_channel()
        super().save(**kwargs)
