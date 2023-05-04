from django.db import models
from apps.apartment.models import Apartment 
from django.contrib.auth import get_user_model

User = get_user_model()

class ApartmentReview(models.Model):
    
    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartment_reviews')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    # sub_comments = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='review_comments')
    
    def __str__(self) -> str:
        return f'Обзор от {self.user.username} на {self.apartment.title}'
    
class ReviewImages(models.Model):
    
    review = models.ForeignKey(ApartmentReview, on_delete=models.CASCADE, related_name='review_images')
    images = models.ImageField(upload_to='images')
    
    class Meta:
        verbose_name = 'Впечатление'
        verbose_name_plural = 'Впечатления'
        

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_likes')
    review = models.ForeignKey(ApartmentReview, on_delete=models.CASCADE, related_name='reviews_likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'review')

    def __str__(self):
        return f'Liked by {self.user.username}'
