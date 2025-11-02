from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from decouple import config


@shared_task
def mailsender(emails: list):
    send_mail(
        subject='Обновление курса',
        message='У нас обновился курс, скорее чекни',
        from_email=config('YANDEX_EMAIL_HOST_USER'),
        recipient_list=emails
    )


@shared_task
def user_is_active_daily_check():
    pass
