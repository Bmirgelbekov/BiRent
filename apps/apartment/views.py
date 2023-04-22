from rest_framework import permissions, viewsets

from .models import Apartment
from .serializers import ApartmentSerializer
from permissions import IsOwner


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filterset_fields = ['category__slug']
    search_fields = ['title']

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.AllowAny]
        elif method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        elif method in ['DELETE', 'PUT', 'PATCH']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    