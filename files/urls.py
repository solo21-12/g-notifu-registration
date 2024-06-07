from rest_framework.routers import DefaultRouter
from .views import FilesViewSet
router = DefaultRouter()
router.register(r'gen_files', FilesViewSet, basename='files')

urlpatterns = router.urls
