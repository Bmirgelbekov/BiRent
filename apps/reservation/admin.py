from django.contrib import admin

from .models import Reservation, ReservationItem


class TabularReservationItem(admin.TabularInline):
    model = ReservationItem
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = [TabularReservationItem]