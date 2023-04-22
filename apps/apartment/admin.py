from django.contrib import admin
from .models import Apartment, ApartmentImage


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage


class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInline]


admin.site.register(Apartment, ApartmentAdmin)