# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
import time  # Для имитации задержки при скачивании

@shared_task
def send_notification_email(email, timestamp):
    # Логика отправки уведомления
    send_mail(
        'Notification',
        'The satelite Landsat starts capturing your zone',
        'landsat.clusterC@gmail.com',
        [email],
        fail_silently=False,
    )

@shared_task
def download_and_send_dataset(email):
    # Логика для скачивания датасета
    time.sleep(10)  # Имитация задержки при скачивании
    # Здесь добавь код для скачивания датасета

    # Логика для отправки датасета по электронной почте
    send_mail(
        'Your dataset',
        'Your dataset is ready',
        'landsat.clusterC@gmail.com',
        [email],
        fail_silently=False,
    )
