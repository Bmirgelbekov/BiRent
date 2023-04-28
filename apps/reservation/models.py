from django.db import models
from apps.apartment.models import Apartment
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_confirmation_mail


User = get_user_model()

# Create your models here.

class ReservationStatus(models.TextChoices):
    opened = 'opened'
    in_process = 'in_process'
    accepted = 'accepted'
    canceled = 'canceled'
    
    
class Reservation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=ReservationStatus.choices)
    
    def __str__(self) -> str:
        return f'бронь №{self.pk}'
    
    class Meta:
        verbose_name = 'Информация о брони'
        verbose_name_plural = 'Информация о бронях'


class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reservated_room')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='reservated_room')
    duration = models.PositiveSmallIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.apartment.title
    
    def save(self, *args, **kwargs):
        self.total_cost = self.duration * self.apartment.price
        return super().save(self, *args, **kwargs)
    
    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'


@receiver(post_save, sender=Reservation)
def send_order_confirmation_mail(sender: Reservation, instance: Reservation, created: bool, **kwargs):
    if created:
        
        send_confirmation_mail.delay(
            instance.user.username,
            instance.pk,
            instance.user.email
        )