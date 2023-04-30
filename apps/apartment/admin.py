from django.contrib import admin
from .models import Apartment, ApartmentImage, Rating


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage


class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInline]

class RatingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Rating, RatingAdmin)