from rest_framework import serializers
from .models import Reservation, ReservationItem


class ReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationItem 
        exclude = ['reservation']
        read_only_fields = ['total_cost']


class ReservationSerializer(serializers.ModelSerializer):
    reservation_items = ReservationItemSerializer(many=True, write_only=True)

    class Meta:
        model = Reservation 
        fields = '__all__'
        read_only_fields = ['total_cost', 'created_at', 'updated_at', 'user', 'status']
        
    def create(self, validated_data):
        query = super().create(validated_data)
        query['reservation_item'] = ReservationItem
        return query