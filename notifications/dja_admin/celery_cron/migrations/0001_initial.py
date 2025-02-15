# Generated by Django 5.0.6 on 2024-05-14 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("django_celery_beat", "0018_improve_crontab_helptext"),
    ]

    operations = [
        migrations.CreateModel(
            name="LateNotif",
            fields=[
                (
                    "clockedschedule_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_celery_beat.clockedschedule",
                    ),
                ),
                (
                    "channel",
                    models.CharField(
                        choices=[("email", "Email"), ("push", "Push")],
                        verbose_name="Способ доставки",
                    ),
                ),
                ("msg_to", models.CharField(max_length=50, verbose_name="Адресат")),
                ("msg_subj", models.CharField(max_length=50, verbose_name="Тема")),
                ("template_id", models.UUIDField(verbose_name="Шаблон")),
                (
                    "template_data",
                    models.TextField(max_length=500, verbose_name="Данные шаблона"),
                ),
            ],
            options={
                "verbose_name_plural": "Отложенные рассылки",
            },
            bases=("django_celery_beat.clockedschedule", models.Model),
        ),
        migrations.CreateModel(
            name="Notif",
            fields=[
                (
                    "clockedschedule_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_celery_beat.clockedschedule",
                    ),
                ),
                (
                    "channel",
                    models.CharField(
                        choices=[("email", "Email"), ("push", "Push")],
                        verbose_name="Способ доставки",
                    ),
                ),
                ("msg_to", models.CharField(max_length=50, verbose_name="Адресат")),
                ("msg_subj", models.CharField(max_length=50, verbose_name="Тема")),
                ("template_id", models.UUIDField(verbose_name="Шаблон")),
                (
                    "template_data",
                    models.TextField(max_length=500, verbose_name="Данные шаблона"),
                ),
            ],
            options={
                "verbose_name_plural": "Рассылки",
            },
            bases=("django_celery_beat.clockedschedule", models.Model),
        ),
        migrations.CreateModel(
            name="PereodicNotif",
            fields=[
                (
                    "periodictask_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_celery_beat.periodictask",
                    ),
                ),
                (
                    "channel",
                    models.CharField(
                        choices=[("email", "Email"), ("push", "Push")],
                        verbose_name="Способ доставки",
                    ),
                ),
                ("msg_to", models.CharField(max_length=50, verbose_name="Адресат")),
                ("msg_subj", models.CharField(max_length=50, verbose_name="Тема")),
                ("template_id", models.UUIDField(verbose_name="Шаблон")),
                (
                    "template_data",
                    models.TextField(max_length=500, verbose_name="Данные шаблона"),
                ),
            ],
            options={
                "verbose_name_plural": "Переодические рассылки",
            },
            bases=("django_celery_beat.periodictask", models.Model),
        ),
    ]
