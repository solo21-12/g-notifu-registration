from rest_framework.routers import DefaultRouter
from .views import Guest

router = DefaultRouter()
router.register(r'', Guest, 'guest')
urlpatterns = router.urls
