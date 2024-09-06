from fastapi import FastAPI
from typing import List
import uvicorn
import os
from celery import Celery
from jinja2 import Environment, FileSystemLoader

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


def email_send(msg_to, msg_subj):
    login = "noreply"
    password = "j4zfn9p3fHcN5qLb8jzU"
    domain = "tz5.ru"
    username = f"{login}@{domain}"
    smtp_server = "smtp.mail.ru"
    port = 465
    current_path = os.path.dirname(__file__)
    loader = FileSystemLoader(current_path)
    env = Environment(loader=loader)

    template = env.get_template("mail.html")

    data = {
        "title": "Новое письмо!",
        "text": "Произошло что-то интересное! :)",
        "image": "https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg",
    }
    body = template.render(**data)

    app = Celery("celery_app", broker="amqp://admin:admin@rabbitmq:5672//")
    data = {
        "smtp_server": smtp_server,
        "port": port,
        "username": username,
        "password": password,
        "msg_to": msg_to,
        "msg_subj": msg_subj,
        "body": body,
    }
    app.send_task("app.send_email", kwargs=data)


@app.post("/send_mail/")
def send_email(msg_to: List[str], msg_subj: str):
    email_send(msg_to, msg_subj)
    return True


def cel_send():
    templ_data = {
        "title": "Новое письмо!",
        "text": "Произошло что-то интересное! :)",
        "image": "https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg",
    }
    msg_to = ["noc@tz5.ru"]
    msg_subj = "test worker"
    template_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    template_data = templ_data
    app = Celery("celery_app", broker="amqp://admin:admin@localhost:5672//")
    data = {
        "msg_to": msg_to,
        "msg_subj": msg_subj,
        "template_id": template_id,
        "template_data": template_data,
    }
    print(data)
    app.send_task("app.send_email", kwargs=data)


if __name__ == "__main__":
    cel_send()
