from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from slugify import slugify


User = get_user_model()


class Apartment(models.Model):
    slug = models.SlugField(primary_key=True, max_length=150, blank=True)
    title = models.CharField(max_length=150)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='apartments'
        )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='images', default='default.jpeg')
    category = models.ForeignKey(
        'category.Category', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='apartments'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug =slugify(self.title) + datetime.now().strftime('_%d_%M_%H')
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        Apartment, 
        on_delete=models.CASCADE, 
        related_name='images'
        )
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусель'

    def __str__(self) -> str:
        return f'image to {self.apartment.title}'


class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    apartment = models.ForeignKey(
        'Apartment', 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    ratings = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ('user', 'apartment')
