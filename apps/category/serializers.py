from rest_framework import serializers
from .models import Category
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['apartments'] = [
            {
                'title': apartment.title, 
                'slug': apartment.slug,
                'user': apartment.user.username,
                'price': apartment.price,
                'main_image': apartment.main_image.url,
                'rating': apartment.ratings.aggregate(Avg('ratings'))['ratings__avg']
            } for apartment in instance.apartments.all()]
        return representation
