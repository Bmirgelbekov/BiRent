from rest_framework import routers

from .views import ReservationViewSet

router = routers.DefaultRouter()
router.register('reservation', ReservationViewSet, 'reservation')

urlpatterns = router.urls