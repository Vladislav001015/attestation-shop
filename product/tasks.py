from django.core.mail import send_mail

from shop_market.celery import app
from .models import Contact
from .services import send

@app.task
def send_spam_email(user_email):
    send(user_email)

@app.task
def send_beat_email():
    for contact in Contact.objects.all():
        send_mail(
            'Вы подписались на рассылку',
            'Мы будем вам отправлять спам',
            'emirfortest@gmail.com',
            [contact.email],
            fail_silently=False,
        )