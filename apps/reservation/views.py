from django.shortcuts import render
from .serializers import ReservationSerializer, ReservationItemSerializer 
from rest_framework import viewsets, permissions


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer