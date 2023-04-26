from django.shortcuts import render
from .serializers import ReservationSerializer, ReservationItemSerializer 
from rest_framework import viewsets, permissions
from .models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer