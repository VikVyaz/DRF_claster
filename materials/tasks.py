from datetime import timedelta

from celery import shared_task
from decouple import config
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def mailsender(emails: list):
    """Задача по рассылке обновление по курсу всем подписчикам"""

    send_mail(
        subject='Обновление курса',
        message='У нас обновился курс, скорее чекни',
        from_email=config('YANDEX_EMAIL_HOST_USER'),
        recipient_list=emails
    )


@shared_task
def user_is_active_daily_check():
    """Периодическая (в 0:00) задача по проверке последнего логина пользователей (не больше 30 дней без активности"""

    cutoff_time = timezone.now() - timedelta(days=30)
    inactive_counter = User.objects.filter(last_login__lt=cutoff_time, is_active=True).update(is_active=False)
    print(f'Пользователей деактивировано: {inactive_counter}')
