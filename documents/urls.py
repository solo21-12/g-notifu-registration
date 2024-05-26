from os import path
from rest_framework.routers import DefaultRouter
from .views import DocuemntViewSet, VehicleManagementViewUser, VehicleWithUser

router = DefaultRouter()
router.register(r'', DocuemntViewSet, basename='document')
router.register(r'owner', VehicleManagementViewUser,
                basename='get_vehicle_documents')
router.register(r'vehicle', VehicleWithUser,
                basename='get_user_vehicle_documents')


urlpatterns = router.urls
