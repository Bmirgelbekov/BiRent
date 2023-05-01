from rest_framework import serializers
from .models import Reservation, ReservationItem


class ReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationItem 
        exclude = ['reservation']
        read_only_fields = ['total_cost']


class ReservationSerializer(serializers.ModelSerializer):
    reservated_room = ReservationItemSerializer(many=True, write_only=True)

    class Meta:
        model = Reservation 
        fields = '__all__'
        read_only_fields = ['total_cost', 'created_at', 'updated_at', 'user', 'status']
        
    def create(self, validated_data: dict):
        validated_data['user'] = self.context.get('request').user
        items = validated_data.pop('reservated_room')
        reservation = Reservation.objects.create(**validated_data)
        total_reservation_cost = 0
        apartments = []
        for item in items:
            apartment = ReservationItem(
                reservation=reservation,
                apartment=item['apartment'],
                duration=item['duration']
            )
            apartments.append(apartment)
            total_reservation_cost += apartment.total_cost
        reservation.total_cost = total_reservation_cost
        ReservationItem.objects.bulk_Create(apartments)
        return reservation