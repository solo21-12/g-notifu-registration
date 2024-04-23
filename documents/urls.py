from rest_framework.routers import DefaultRouter
from .views import DocuemntViewSet

router = DefaultRouter()
router.register(r'', DocuemntViewSet, basename='document')

urlpatterns = router.urls
