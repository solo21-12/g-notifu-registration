from rest_framework.routers import DefaultRouter
from .views import AddVehicleViewSet, ManageVehicleViewSet, VehicleListView
router = DefaultRouter()
# router.register(r'', VehicleViewSet, basename='vehicle')
router.register(r'add_vehicle', AddVehicleViewSet, basename='add_vehicle')
router.register(r'', ManageVehicleViewSet, basename='vehicel')
router.register(r'owner_vehicle', VehicleListView, basename='owner_vehicle')
urlpatterns = router.urls
