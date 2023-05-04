from rest_framework import viewsets, mixins, permissions

from .models import Faciliti
from .serializers import FacilitiSerializer


class FacilitiCreateReadDeleteView(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin,
                                   viewsets.GenericViewSet):
    queryset = Faciliti.objects.all()
    serializer_class = FacilitiSerializer

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.AllowAny]
        elif method in ['POST', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
