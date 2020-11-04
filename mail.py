import os
from flask_mail import Mail, Message

from app import app


mail = Mail(app)

def send_order_mail(email, username, order):
    with app.app_context():
        text_body = f"{username}! Ваш заказ ({', '.join(order)}) был сформирован и отправлен на обработку."
        msg = Message(
            subject="Stepik Delivery",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email]
        )
        msg.body = text_body
        mail.send(msg)