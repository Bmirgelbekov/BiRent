from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['apartments'] = [
    #         {'title': apartment.title, 'slug': apartment.slug} for apartment in instance.apartments.all()]
    #     return representation
