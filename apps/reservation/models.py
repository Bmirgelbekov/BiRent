from django.db import models
from apps.apartment.models import Apartment
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class ReservationStatus(models.TextChoices):
    opened = 'opened'
    in_process = 'in_process'
    accepted = 'accepted'
    canceled = 'canceled'

    
class ReservationItem(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='reservated_room')
    
    
class Reservation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=10, choices=ReservationStatus.choices)
    duration = models.PositiveIntegerField(default=1)
    
    
    def save(self, *args, **kwargs):
        self.total_cost = self.duration * self.ReservationItem.apartment.price 
        return super().save(self, *args, **kwargs)
    
    def __str__(self) -> str:
        return f'бронь №{self.pk}'
    
    class Meta:
        verbose_name = 'информация о брони'
        verbose_name_plural = 'информация о бронях'