from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_confirmation_mail(username, pk, email):
    message =f""" 
     Здравствуйте, {username}!
     Подтвердите бронь на сайте BiRent,

     http://localhost:8000/reservation/{pk}/confirm/

     Если это были не Вы, игнорируйте это сообщение
       """
    send_mail(
        subject='Подтверждение брони',
        message=message,
        from_email='test@test.com',
        recipient_list=[email],
        fail_silently=False
    )
