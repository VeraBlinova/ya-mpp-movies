import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from uuid import uuid4

from config import settings
from get_user import get_email
from models.notifications import Notification

from db import get_db_session


async def on_message(message):
    async with message.process():
        decoded = message.body.decode()
        logging.info("Received message:", decoded)
        email = get_email(message.to_dict()["user_id"])
        _send_email(email, decoded)
        await _save_notification(decoded, email)


async def _save_notification(message, email: str):
    session = get_db_session()
    notification = Notification(
        notification_id=uuid4(),
        content_id=uuid4(),
        recipient_email=email,
        text=message,
        created_at=datetime.utcnow(),
        type="email",
        schedule_id=uuid4(),
    )
    session.add(notification)
    await session.commit()
    await session.refresh(notification)


def _send_email(to_email: str, message: str):
    smtp_server = settings.smtp.host
    from_email = settings.smtp.user

    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Hello"
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server) as server:
        server.send_message(msg)
