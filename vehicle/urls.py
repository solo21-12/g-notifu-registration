from rest_framework.routers import DefaultRouter
from .views import AddVehicleViewSet, ManageVehicleViewSet, VehicleListView

router = DefaultRouter()
router.register(r'get_vehicle', ManageVehicleViewSet, basename='vehicle')
router.register(r'add_vehicle', AddVehicleViewSet, basename='add_vehicle')
router.register(r'owner_vehicle', VehicleListView, basename='owner_vehicle')
urlpatterns = router.urls
