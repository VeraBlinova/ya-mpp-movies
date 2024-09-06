import json
import logging
import smtplib
from email.message import EmailMessage
from os import environ
from uuid import UUID

import requests
from celery_cron.get_user import get_email
from jinja2 import Template

smtp_server = environ["SMTP_SERVER"]
smtp_port = environ["SMTP_PORT"]
smtp_user = environ["SMTP_USER"]
smtp_pass = environ["SMTP_PASS"]

logger = logging.getLogger(__name__)


class EmailSender:

    def __init__(self, msg_to: str, msg_subj: str, template_id: UUID, template_data: str):
        self.mst_to = msg_to
        self.user_name = smtp_user
        self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        self.server.login(smtp_user, smtp_pass)
        self.message = EmailMessage()
        self.message["From"] = smtp_user
        self.message["Subject"] = msg_subj

        template_url = f"{environ.get('TEMPLATE_URL')}{template_id}"
        response = requests.get(template_url)
        template_body = response.content.decode().strip('"')
        template = Template(template_body)
        body = template.render(json.loads(template_data))
        self.message.add_alternative(body, subtype="html")

    def send(self):
        for user_id in self.mst_to.split(";"):
            try:
                addr = get_email(user_id)
            except Exception as e:
                logger.error(f"No user {user_id} profile: {e}")
                addr = user_id
            try:
                self.server.sendmail(self.user_name, addr, self.message.as_string())
            except smtplib.SMTPException as exc:
                reason = f"{type(exc).__name__}: {exc}"
                logger.error(f"Не удалось отправить письмо. {reason}")
            else:
                logger.info("Письмо отправлено!")

    def __exit__(self):
        self.server.close()


def get_sender(**kwargs):
    sender = EmailSender(**kwargs)
    sender.send()
