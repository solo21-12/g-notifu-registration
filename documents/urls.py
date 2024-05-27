from os import path
from rest_framework.routers import DefaultRouter
from .views import DocuemntViewSet, VehicleManagementViewUser, VehicleWithUser, RoadFundDocumentRenew, InsuranceDocumentRenew

router = DefaultRouter()
router.register(r'', DocuemntViewSet, basename='document')
router.register(r'owner', VehicleManagementViewUser,
                basename='get_vehicle_documents')
router.register(r'vehicle', VehicleWithUser,
                basename='get_user_vehicle_documents')
router.register(r'renew_road_fund', RoadFundDocumentRenew,
                basename="renew_road_fund")
router.register(r'renew_insurance', InsuranceDocumentRenew,
                basename="renew_insurance")

urlpatterns = router.urls
