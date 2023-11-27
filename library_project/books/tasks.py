from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(email, username):
    send_mail(
        'Welcome to our Book Library',
        f'Hello {username}, welcome to our book library!',
        'from@example.com',
        [email],
        fail_silently=False,
    )