from rest_framework.routers import DefaultRouter
from .views import AddVehicleViewSet, ManageVehicleViewSet
router = DefaultRouter()
# router.register(r'', VehicleViewSet, basename='vehicle')
router.register(r'add_vehicle', AddVehicleViewSet, basename='add_vehicle')
router.register(r'', ManageVehicleViewSet, basename='vehicel')
urlpatterns = router.urls
