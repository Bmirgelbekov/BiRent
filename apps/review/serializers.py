from rest_framework import serializers 
from .models import ApartmentReview, ReviewImages, Like

class ApartmentReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ApartmentReview
        fields = '__all__'
        read_only_fields = ['id', 'user', 'sub_comment']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        

class ReviewListSerializer(serializers.ListSerializer):
    
    child_serializer = ApartmentReviewSerializer()
    
    
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Like 
        fields = ['user', 'review']
        
