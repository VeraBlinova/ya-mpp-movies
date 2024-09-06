from django.contrib import admin

from .models import LateNotif, Notif, PereodicNotif


@admin.register(Notif)
class NotifAdmin(admin.ModelAdmin):
    fields = ("channel", "msg_to", "msg_subj", "template_id", "template_data")


@admin.register(LateNotif)
class LateNotifAdmin(admin.ModelAdmin):
    fields = (
        "channel",
        "msg_to",
        "msg_subj",
        "template_id",
        "template_data",
        "clocked_time",
    )


@admin.register(PereodicNotif)
class PereodicNotifAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "enabled",
        "channel",
        "msg_to",
        "msg_subj",
        "template_id",
        "template_data",
        "start_time",
        "one_off",
        "crontab",
        "expires",
    )
