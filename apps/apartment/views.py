from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from permissions import IsOwner

from .models import Apartment, Rating
from .serializers import ApartmentSerializer, RatingSerializer


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filterset_fields = ['category__slug']
    search_fields = ['title']

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.AllowAny]
        elif method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        elif method in ['DELETE', 'PUT', 'PATCH']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    

    @action(detail=False, methods=['GET'])
    def get_novelties(self, request):
        apartments = Apartment.objects.order_by('-created_at')[:8]
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def get_popular(self, request):
        apartments = Apartment.objects.exclude(ratings__isnull=True).annotate(avg_rating=Avg('ratings__ratings')).order_by('-avg_rating')[:8]
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path='users/(?P<user_id>\d+)/apartments')
    def get_user_apartments(self, request, user_id=None):
        apartments = Apartment.objects.filter(user_id=user_id)
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)
    

class RateApartment(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        apartment = get_object_or_404(Apartment, slug=slug)
        rating_value = request.data.get('ratings')

        if not rating_value or rating_value not in [1, 2, 3, 4, 5]:
            raise ValidationError('Please provide a valid ratings value (1-5).')

        ratings, created = Rating.objects.get_or_create(
            user=request.user,
            apartment=apartment,
            defaults={'ratings': rating_value}
        )

        if not created:
            ratings.ratings = rating_value
            ratings.save()

        serializer = RatingSerializer(ratings)
        return Response(serializer.data)
