from rest_framework import permissions, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response  import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from .models import Apartment, Rating
from .serializers import ApartmentSerializer, RatingSerializer
from permissions import IsOwner
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


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
        apartments = Apartment.objects.order_by('-created_at')[:10]
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def get_popular(self, request):
        apartment = Apartment.objects.annotate(avg_rating=Avg('ratings')).order_by('-avg_rating')
        serializer = ApartmentSerializer(apartment, many=True)
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