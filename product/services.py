from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку новых товаров',
        'Мы будем вам сообщать о новых товарах',
        'emirfortest@gmail.com',
        [user_email],
        fail_silently=False,
    )