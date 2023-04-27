from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ReservationSerializer, ReservationItemSerializer 
from .models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user.pk)
    
    @action(methods=['GET'], detail=True)
    def confirm(self, request, pk):
        order = Reservation.objects.get(pk=pk)
        order.status = 'in_process'
        order.save()
        return Response({'message': 'Бронь в процессе обработки'}, status=200)
    
    def get_permissions(self):
        if self.action == 'confirm':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()