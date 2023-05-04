from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ReviewListSerializer, ApartmentReviewSerializer
from .models import ApartmentReview, Like


class ApartmentReviewViewSet(ModelViewSet):
     
    serializer_class = ApartmentReviewSerializer 
     
    def get_queryset(self):
        return ApartmentReview.objects.filter(user=self.request.user.pk)
    
    @action(methods=['POST'], detail=True)
    def put_like(self, request, pk=None):
        review = self.get_object()
        like = Like.objects.filter(user=request.user, review=review)
        if like.exists():
            like.delete()
            return Response({'Liked': False})
        else:
            Like.objects.create(request=request.user, review=review).save()
            return Response({'Likes': True})