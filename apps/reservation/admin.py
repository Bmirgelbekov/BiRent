from django.contrib import admin
from .models import Reservation, ReservationItem

# Register your models here.

admin.site.register([Reservation, ReservationItem])