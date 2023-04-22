from rest_framework import routers

from .views import ApartmentViewSet


router = routers.DefaultRouter()
router.register('apartment', ApartmentViewSet, 'apartment')

urlpatterns = router.urls