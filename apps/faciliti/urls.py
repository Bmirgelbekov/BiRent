from rest_framework import routers
from .views import FacilitiCreateReadDeleteView

router = routers.DefaultRouter()
router.register('facilities', FacilitiCreateReadDeleteView, 'facilities')

urlpatterns = router.urls