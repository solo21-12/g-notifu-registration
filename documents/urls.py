from os import path
from rest_framework.routers import DefaultRouter
from .views import DocuemntViewSet, VehicleManagementViewUser, VehicleWithUser, RoadFundDocumentRenew, InsuranceDocumentRenew,RoadAuthorityDocumentRenew

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
router.register(r'renew_road_authority', RoadAuthorityDocumentRenew,
                basename="renew_road_authority")

urlpatterns = router.urls
