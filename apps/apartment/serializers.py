from rest_framework import serializers
from .models import Apartment, ApartmentImage
from django.db import models


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ['image']


class ApartmentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        return [{
            'title': item.title,
            'slug': item.slug,
            'user': item.user.username,
            'price': item.price,
            'main_image': item.main_image.url
        } for item in iterable]


class ApartmentSerializer(serializers.ModelSerializer):
    imgs = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Apartment
        fields = '__all__'
        # exclude = 'поле которое нужно пропустить'
        read_only_fields = ['slug']
        list_serializer_class = ApartmentListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['carousel'] = ApartmentImageSerializer(
                                        instance.images.all(),
                                        many=True
                                        ).data
        return representation

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        imgs = validated_data.pop('imgs', None)
        apartment = Apartment.objects.create(**validated_data)
        if imgs is not None:
            images = []
            for image in imgs:
                images.append(ApartmentImage(apartment=apartment, image=image))
            ApartmentImage.objects.bulk_create(images)
        return apartment