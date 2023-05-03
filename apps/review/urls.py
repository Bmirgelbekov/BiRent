from rest_framework import routers

from .views import ApartmentReviewViewSet

router = routers.DefaultRouter()
router.register('review', ApartmentReviewViewSet, 'review')

urlpatterns = router.urls 